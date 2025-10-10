#!/usr/bin/env python3
"""
Authentication Testing Script for EscolaLMS API
Tests all authentication flows to determine if auth is working or broken
"""

import json
import base64
import time
import requests
import sys
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

# Configuration
API_BASE_URL = "http://api.localhost"
TEST_CREDENTIALS = {
    "admin": {"email": "admin2@escolalms.com", "password": "secret"},
    "student": {"email": "student@escolalms.com", "password": "secret"},
}

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class AuthenticationTester:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.current_token = None
        self.test_results = {
            "login": {},
            "token_validation": {},
            "protected_endpoints": {},
            "configuration": {},
            "summary": {}
        }

    def print_header(self, text: str):
        """Print a formatted header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

    def print_test(self, name: str, status: bool, details: str = ""):
        """Print test result with color coding"""
        status_text = f"{Colors.GREEN}✓ PASS{Colors.ENDC}" if status else f"{Colors.FAIL}✗ FAIL{Colors.ENDC}"
        print(f"  {name}: {status_text}")
        if details:
            print(f"    {Colors.CYAN}{details}{Colors.ENDC}")

    def decode_jwt(self, token: str) -> Optional[Dict[str, Any]]:
        """Decode JWT token payload without verification"""
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return None

            payload = parts[1]
            # Add padding if needed
            payload += '=' * (4 - len(payload) % 4)
            decoded = base64.b64decode(payload)
            return json.loads(decoded)
        except Exception as e:
            print(f"    {Colors.WARNING}Error decoding JWT: {e}{Colors.ENDC}")
            return None

    def test_login(self, email: str, password: str) -> Tuple[bool, Optional[str]]:
        """Test login endpoint"""
        self.print_header(f"PHASE 1: Testing Login ({email})")

        try:
            response = requests.post(
                f"{self.base_url}/api/auth/login",
                headers={"Content-Type": "application/json"},
                json={"email": email, "password": password}
            )

            data = response.json()

            # Test: Response status
            self.print_test(
                "HTTP Status 200",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )

            # Test: Success field
            success = data.get("success", False)
            self.print_test("Success field", success, f"success: {success}")

            # Test: Token exists
            token = data.get("data", {}).get("token")
            has_token = bool(token)
            self.print_test("Token received", has_token, f"Token length: {len(token) if token else 0}")

            if token:
                # Decode and analyze token
                payload = self.decode_jwt(token)
                if payload:
                    exp_time = payload.get("exp", 0)
                    current_time = time.time()
                    minutes_until_expiry = (exp_time - current_time) / 60

                    self.print_test(
                        "JWT decoding",
                        True,
                        f"User ID: {payload.get('sub')}, Expires in: {minutes_until_expiry:.1f} minutes"
                    )

                    # Test: Token expiry time
                    self.print_test(
                        "Token expiry",
                        minutes_until_expiry > 0,
                        f"{'Valid' if minutes_until_expiry > 0 else 'Expired'}"
                    )

                    # Store results
                    self.test_results["login"][email] = {
                        "success": success,
                        "token_received": has_token,
                        "user_id": payload.get("sub"),
                        "expiry_minutes": minutes_until_expiry
                    }
                else:
                    self.print_test("JWT decoding", False, "Failed to decode")

                self.current_token = token
                return success and has_token, token

            return False, None

        except Exception as e:
            self.print_test("Login request", False, str(e))
            return False, None

    def test_protected_endpoint(self, endpoint: str, token: str, method: str = "GET") -> bool:
        """Test a protected endpoint with token"""
        try:
            headers = {"Authorization": f"Bearer {token}"}

            if method == "GET":
                response = requests.get(f"{self.base_url}{endpoint}", headers=headers)
            else:
                response = requests.post(f"{self.base_url}{endpoint}", headers=headers)

            success = response.status_code == 200

            # Parse response
            try:
                data = response.json()
                message = data.get("message", "")

                # Check for specific auth failure messages
                is_authenticated = "Unauthenticated" not in message

                details = f"Status: {response.status_code}"
                if not is_authenticated:
                    details += f" - {message}"
                elif success:
                    if "data" in data:
                        if isinstance(data["data"], list):
                            details += f" - {len(data['data'])} items"
                        elif isinstance(data["data"], dict):
                            details += f" - User: {data['data'].get('email', 'unknown')}"

            except:
                is_authenticated = success
                details = f"Status: {response.status_code}"

            self.print_test(endpoint, is_authenticated, details)

            # Store result
            if endpoint not in self.test_results["protected_endpoints"]:
                self.test_results["protected_endpoints"][endpoint] = {}
            self.test_results["protected_endpoints"][endpoint] = {
                "authenticated": is_authenticated,
                "status_code": response.status_code,
                "message": message if 'message' in locals() else ""
            }

            return is_authenticated

        except Exception as e:
            self.print_test(endpoint, False, str(e))
            return False

    def test_all_protected_endpoints(self, token: str):
        """Test all known protected endpoints"""
        self.print_header("PHASE 2: Testing Protected Endpoints")

        endpoints = [
            # Profile endpoints
            ("/api/profile/me", "GET"),
            ("/api/profile/settings", "GET"),

            # Auth endpoints
            ("/api/auth/refresh", "GET"),
            ("/api/auth/logout", "POST"),

            # Course endpoints
            ("/api/courses/my", "GET"),
            ("/api/courses/progress", "GET"),

            # Admin endpoints
            ("/api/admin/courses", "GET"),
            ("/api/admin/users", "GET"),
            ("/api/admin/categories", "GET"),

            # User management
            ("/api/admin/user-groups", "GET"),
        ]

        working_count = 0
        for endpoint, method in endpoints:
            if self.test_protected_endpoint(endpoint, token, method):
                working_count += 1

        print(f"\n  {Colors.BOLD}Summary: {working_count}/{len(endpoints)} endpoints working{Colors.ENDC}")
        self.test_results["summary"]["working_endpoints"] = working_count
        self.test_results["summary"]["total_endpoints"] = len(endpoints)

    def check_configuration(self):
        """Check various configuration aspects"""
        self.print_header("PHASE 3: Configuration Checks")

        # Test public endpoints
        print(f"{Colors.CYAN}Testing public endpoints (no auth required):{Colors.ENDC}")

        public_endpoints = [
            "/api/courses",
            "/api/categories",
        ]

        for endpoint in public_endpoints:
            try:
                response = requests.get(f"{self.base_url}{endpoint}")
                success = response.status_code == 200
                self.print_test(endpoint, success, f"Status: {response.status_code}")
            except Exception as e:
                self.print_test(endpoint, False, str(e))

        # Test CORS headers
        print(f"\n{Colors.CYAN}Testing CORS configuration:{Colors.ENDC}")
        try:
            response = requests.options(
                f"{self.base_url}/api/admin/courses",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "GET",
                    "Access-Control-Request-Headers": "authorization"
                }
            )

            cors_headers = {
                "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
                "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers"),
                "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
            }

            for header, value in cors_headers.items():
                self.print_test(header, bool(value), value or "Not set")

        except Exception as e:
            self.print_test("CORS test", False, str(e))

    def test_alternative_credentials(self):
        """Test with different user credentials"""
        self.print_header("PHASE 4: Alternative User Testing")

        # Try student account
        success, token = self.test_login(
            TEST_CREDENTIALS["student"]["email"],
            TEST_CREDENTIALS["student"]["password"]
        )

        if success and token:
            print(f"\n{Colors.CYAN}Testing student endpoints:{Colors.ENDC}")
            self.test_protected_endpoint("/api/profile/me", token)
            self.test_protected_endpoint("/api/courses/my", token)
            # Student shouldn't access admin endpoints
            self.test_protected_endpoint("/api/admin/courses", token)

    def generate_summary(self):
        """Generate final summary and recommendations"""
        self.print_header("FINAL ANALYSIS")

        # Determine overall status
        login_works = any(
            result.get("success", False)
            for result in self.test_results["login"].values()
        )

        endpoints_work = self.test_results["summary"].get("working_endpoints", 0) > 0

        profile_works = self.test_results["protected_endpoints"].get("/api/profile/me", {}).get("authenticated", False)
        admin_works = self.test_results["protected_endpoints"].get("/api/admin/courses", {}).get("authenticated", False)

        print(f"{Colors.BOLD}Authentication Status:{Colors.ENDC}")
        print(f"  • Login: {Colors.GREEN if login_works else Colors.FAIL}{'Working' if login_works else 'Broken'}{Colors.ENDC}")
        print(f"  • Token Generation: {Colors.GREEN if login_works else Colors.FAIL}{'Working' if login_works else 'Broken'}{Colors.ENDC}")
        print(f"  • Profile Endpoint: {Colors.GREEN if profile_works else Colors.FAIL}{'Working' if profile_works else 'Broken'}{Colors.ENDC}")
        print(f"  • Admin Endpoints: {Colors.GREEN if admin_works else Colors.FAIL}{'Working' if admin_works else 'Broken'}{Colors.ENDC}")

        print(f"\n{Colors.BOLD}Hybrid Mode Readiness:{Colors.ENDC}")

        if profile_works:
            print(f"  {Colors.GREEN}✓ Authentication is PARTIALLY WORKING{Colors.ENDC}")
            print(f"    - JWT tokens are valid and can be used")
            print(f"    - User profile can be retrieved")
            print(f"    - Hybrid mode CAN be implemented")

            if not admin_works:
                print(f"  {Colors.WARNING}⚠ Some endpoints have issues:{Colors.ENDC}")
                print(f"    - Admin endpoints may require additional permissions")
                print(f"    - Consider using role detection from /api/profile/me")
        else:
            print(f"  {Colors.FAIL}✗ Authentication is BROKEN{Colors.ENDC}")
            print(f"    - Tokens are generated but not validated properly")
            print(f"    - Hybrid mode needs auth to be fixed first")

        # Save results to file
        with open("/home/pree/Code/Thrive/EscolaAPI/apidoc/scripts/auth_test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)

        print(f"\n{Colors.CYAN}Full results saved to: auth_test_results.json{Colors.ENDC}")

def main():
    """Run all authentication tests"""
    tester = AuthenticationTester()

    print(f"{Colors.BOLD}{Colors.CYAN}EscolaLMS Authentication Testing Suite{Colors.ENDC}")
    print(f"{Colors.CYAN}Testing API at: {API_BASE_URL}{Colors.ENDC}")
    print(f"{Colors.CYAN}Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")

    # Test admin login
    success, token = tester.test_login(
        TEST_CREDENTIALS["admin"]["email"],
        TEST_CREDENTIALS["admin"]["password"]
    )

    if success and token:
        # Test all protected endpoints with admin token
        tester.test_all_protected_endpoints(token)
    else:
        print(f"\n{Colors.FAIL}Login failed - cannot test protected endpoints{Colors.ENDC}")

    # Test configuration
    tester.check_configuration()

    # Test alternative credentials
    tester.test_alternative_credentials()

    # Generate summary
    tester.generate_summary()

    # Return exit code based on results
    if tester.test_results["summary"].get("working_endpoints", 0) > 0:
        sys.exit(0)  # Some things work
    else:
        sys.exit(1)  # Complete failure

if __name__ == "__main__":
    main()