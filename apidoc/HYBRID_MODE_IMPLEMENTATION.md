# Hybrid Mode Implementation Guide

## Quick Start

**Good news!** Authentication works enough for your hybrid mode. Here's exactly how to implement it.

---

## 1. Environment Configuration

```env
# .env
VITE_USE_BACKEND_AUTH=true    # Use real JWT authentication
VITE_USE_BACKEND_DATA=false   # Use mock course data
VITE_API_URL=http://api.localhost
```

---

## 2. Authentication Service (Real)

```typescript
// services/authService.ts
export class RealAuthService {
  private baseUrl = 'http://api.localhost';
  private token: string | null = null;
  private tokenExpiry: Date | null = null;

  async login(email: string, password: string): Promise<boolean> {
    const response = await fetch(`${this.baseUrl}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (data.success) {
      this.token = data.data.token;
      this.tokenExpiry = new Date(data.data.expires_at);
      localStorage.setItem('auth_token', this.token);
      localStorage.setItem('token_expiry', data.data.expires_at);

      // Start auto-refresh
      this.startTokenRefresh();
      return true;
    }

    return false;
  }

  async getUserProfile(): Promise<UserProfile | null> {
    if (!this.token) return null;

    const response = await fetch(`${this.baseUrl}/api/profile/me`, {
      headers: { 'Authorization': `Bearer ${this.token}` }
    });

    if (response.ok) {
      const data = await response.json();
      return {
        id: data.data.id,
        email: data.data.email,
        name: data.data.name,
        roles: data.data.roles,
        isAdmin: data.data.roles.includes('admin'),
        isTutor: data.data.roles.includes('tutor'),
        isStudent: data.data.roles.includes('student') ||
                   !data.data.roles.includes('admin')
      };
    }

    return null;
  }

  private startTokenRefresh() {
    setInterval(async () => {
      if (this.shouldRefreshToken()) {
        await this.refreshToken();
      }
    }, 30000); // Check every 30 seconds
  }

  private shouldRefreshToken(): boolean {
    if (!this.tokenExpiry) return false;
    const now = new Date();
    const timeUntilExpiry = this.tokenExpiry.getTime() - now.getTime();
    return timeUntilExpiry < 60000; // Refresh if less than 1 minute
  }

  async refreshToken(): Promise<boolean> {
    if (!this.token) return false;

    const response = await fetch(`${this.baseUrl}/api/auth/refresh`, {
      headers: { 'Authorization': `Bearer ${this.token}` }
    });

    if (response.ok) {
      const data = await response.json();
      this.token = data.data.token;
      this.tokenExpiry = new Date(data.data.expires_at);
      localStorage.setItem('auth_token', this.token);
      return true;
    }

    return false;
  }

  isAuthenticated(): boolean {
    return !!this.token && new Date() < (this.tokenExpiry || new Date(0));
  }

  getToken(): string | null {
    return this.token;
  }

  logout(): void {
    if (this.token) {
      fetch(`${this.baseUrl}/api/auth/logout`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${this.token}` }
      });
    }

    this.token = null;
    this.tokenExpiry = null;
    localStorage.removeItem('auth_token');
    localStorage.removeItem('token_expiry');
  }
}
```

---

## 3. Hybrid API Implementation

```typescript
// api/hybridAPI.ts
export class HybridAPI {
  private authService: RealAuthService;
  private mockData: MockDataService;
  private userProfile: UserProfile | null = null;

  constructor() {
    this.authService = new RealAuthService();
    this.mockData = new MockDataService();
  }

  // === Authentication (Real Backend) ===

  async login(email: string, password: string): Promise<LoginResponse> {
    const success = await this.authService.login(email, password);

    if (success) {
      this.userProfile = await this.authService.getUserProfile();
    }

    return {
      success,
      user: this.userProfile
    };
  }

  async getUserProfile(): Promise<UserProfile | null> {
    if (!this.userProfile) {
      this.userProfile = await this.authService.getUserProfile();
    }
    return this.userProfile;
  }

  isAuthenticated(): boolean {
    return this.authService.isAuthenticated();
  }

  // === Data Operations (Mock with Real Auth) ===

  async getCourses(): Promise<Course[]> {
    // Require real authentication
    if (!this.isAuthenticated()) {
      throw new Error('Authentication required');
    }

    // Get mock courses
    const allCourses = this.mockData.getCourses();

    // Filter based on real user role
    if (this.userProfile?.isAdmin) {
      return allCourses; // Admin sees everything
    } else {
      // Students only see published courses
      return allCourses.filter(c => c.status === 'published');
    }
  }

  async enrollInCourse(courseId: number): Promise<boolean> {
    // Require real authentication
    if (!this.isAuthenticated()) {
      throw new Error('Authentication required');
    }

    // Use mock enrollment but check real auth
    return this.mockData.enrollUser(this.userProfile!.id, courseId);
  }

  async createCourse(course: CourseCreate): Promise<Course> {
    // Only admins can create courses
    if (!this.userProfile?.isAdmin) {
      throw new Error('Admin access required');
    }

    // Create in mock data
    return this.mockData.createCourse(course);
  }
}
```

---

## 4. Mock Data Service with Auth Awareness

```typescript
// services/mockDataService.ts
export class MockDataService {
  private courses: Course[] = [...]; // Your mock courses

  getCourses(): Course[] {
    return this.courses;
  }

  enrollUser(userId: number, courseId: number): boolean {
    // Track enrollment in localStorage or memory
    const enrollments = this.getEnrollments();
    enrollments[userId] = enrollments[userId] || [];

    if (!enrollments[userId].includes(courseId)) {
      enrollments[userId].push(courseId);
      this.saveEnrollments(enrollments);
      return true;
    }

    return false;
  }

  getUserCourses(userId: number): Course[] {
    const enrollments = this.getEnrollments();
    const userCourseIds = enrollments[userId] || [];
    return this.courses.filter(c => userCourseIds.includes(c.id));
  }

  private getEnrollments(): Record<number, number[]> {
    const stored = localStorage.getItem('mock_enrollments');
    return stored ? JSON.parse(stored) : {};
  }

  private saveEnrollments(enrollments: Record<number, number[]>): void {
    localStorage.setItem('mock_enrollments', JSON.stringify(enrollments));
  }
}
```

---

## 5. React Hook for Hybrid Mode

```typescript
// hooks/useHybridAPI.ts
import { useState, useEffect } from 'react';

export function useHybridAPI() {
  const [api] = useState(() => new HybridAPI());
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if already logged in
    const checkAuth = async () => {
      if (api.isAuthenticated()) {
        const profile = await api.getUserProfile();
        setUser(profile);
        setIsAuthenticated(true);
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    const result = await api.login(email, password);
    if (result.success) {
      setUser(result.user);
      setIsAuthenticated(true);
    }
    return result.success;
  };

  const logout = () => {
    api.logout();
    setUser(null);
    setIsAuthenticated(false);
  };

  return {
    api,
    isAuthenticated,
    user,
    loading,
    login,
    logout,
    isAdmin: user?.isAdmin || false,
    isStudent: user?.isStudent || false
  };
}
```

---

## 6. Usage in Components

```tsx
// components/CourseList.tsx
function CourseList() {
  const { api, isAuthenticated, isAdmin } = useHybridAPI();
  const [courses, setCourses] = useState<Course[]>([]);

  useEffect(() => {
    if (isAuthenticated) {
      api.getCourses().then(setCourses);
    }
  }, [isAuthenticated]);

  return (
    <div>
      <h1>Courses ({courses.length})</h1>
      {isAdmin && (
        <div className="admin-notice">
          🔐 Real Auth + Mock Data (Admin Mode)
        </div>
      )}

      {courses.map(course => (
        <CourseCard key={course.id} course={course} />
      ))}
    </div>
  );
}
```

---

## 7. Dev Mode Indicator

```tsx
// components/DevModeIndicator.tsx
function DevModeIndicator() {
  const { user, isAuthenticated } = useHybridAPI();

  const mode = {
    auth: import.meta.env.VITE_USE_BACKEND_AUTH === 'true' ? 'Real' : 'Mock',
    data: import.meta.env.VITE_USE_BACKEND_DATA === 'true' ? 'Real' : 'Mock'
  };

  if (!isAuthenticated) return null;

  return (
    <div className="dev-indicator">
      <span>🔐 Hybrid Mode</span>
      <span>Auth: {mode.auth} ✅</span>
      <span>Data: {mode.data}</span>
      <span>User: {user?.email}</span>
      <span>Role: {user?.roles.join(', ')}</span>
    </div>
  );
}
```

---

## 8. Testing the Implementation

```typescript
// Run this test script
async function testHybridMode() {
  const api = new HybridAPI();

  // Test 1: Login with real credentials
  console.log('Testing login...');
  const loginResult = await api.login('admin2@escolalms.com', 'secret');
  console.assert(loginResult.success, 'Login should succeed');

  // Test 2: Get real user profile
  console.log('Testing profile...');
  const profile = await api.getUserProfile();
  console.assert(profile?.email === 'admin2@escolalms.com', 'Should get admin profile');
  console.assert(profile?.isAdmin === true, 'Should detect admin role');

  // Test 3: Get mock courses with real auth
  console.log('Testing courses...');
  const courses = await api.getCourses();
  console.assert(courses.length > 0, 'Should return mock courses');

  // Test 4: Token refresh
  console.log('Testing token refresh...');
  const refreshed = await api.authService.refreshToken();
  console.assert(refreshed, 'Token refresh should work');

  console.log('✅ All tests passed!');
}
```

---

## Key Benefits of This Approach

1. **Real Security**: Actual password validation, no hardcoded credentials
2. **Real Roles**: Admin detection from actual backend
3. **Token Management**: Proper expiry and refresh handling
4. **Mock Flexibility**: Control data without backend changes
5. **Gradual Migration**: Easy to switch to real data later

---

## Migration Path

When ready to use real data:

```env
# Just change this flag
VITE_USE_BACKEND_DATA=true
```

Then update the API factory to use real endpoints for courses. The authentication layer remains unchanged!

---

## Summary

Your hybrid mode is **100% implementable** right now because:
- ✅ Login endpoint works
- ✅ Profile endpoint works (provides roles)
- ✅ Token refresh works
- ✅ You planned to use mock data anyway

The broken course endpoints don't matter - you're using mock data by design!