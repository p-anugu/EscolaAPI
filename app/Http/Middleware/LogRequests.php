<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class LogRequests
{
    public function handle(Request $request, Closure $next)
    {
        $startTime = microtime(true);

        // Log incoming request
        Log::info('Incoming Request', [
            'method' => $request->method(),
            'uri' => $request->getRequestUri(),
            'path' => $request->path(),
            'ip' => $request->ip(),
            'user_agent' => $request->userAgent(),
            'headers' => [
                'authorization' => $request->header('Authorization') ? 'Bearer ***' : 'none',
                'content_type' => $request->header('Content-Type'),
                'accept' => $request->header('Accept'),
                'origin' => $request->header('Origin'),
            ],
            'user_id' => $request->user() ? $request->user()->id : null,
        ]);

        $response = $next($request);

        $duration = round((microtime(true) - $startTime) * 1000, 2);

        // Log response
        Log::info('Outgoing Response', [
            'method' => $request->method(),
            'uri' => $request->getRequestUri(),
            'status' => $response->getStatusCode(),
            'duration_ms' => $duration,
            'user_id' => $request->user() ? $request->user()->id : null,
        ]);

        return $response;
    }
}