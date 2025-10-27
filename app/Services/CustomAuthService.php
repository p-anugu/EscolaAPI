<?php

namespace App\Services;

use EscolaLms\Auth\Models\User;
use EscolaLms\Auth\Services\AuthService;
use Laravel\Passport\Passport;
use Laravel\Passport\PersonalAccessTokenResult;

class CustomAuthService extends AuthService
{
    /**
     * Override token creation to always use 30-day expiration
     * This ensures admins don't get logged out while creating courses
     *
     * @param User $user
     * @param bool $rememberMe Ignored - always uses 30-day tokens
     * @return PersonalAccessTokenResult
     */
    public function createTokenForUser(User $user, bool $rememberMe = false): PersonalAccessTokenResult
    {
        // Always set 30-day expiration regardless of rememberMe parameter
        Passport::personalAccessTokensExpireIn(now()->addMonth());

        return $user->createToken(config('passport.personal_access_client.secret'));
    }
}
