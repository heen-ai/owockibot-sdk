"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ServerError = exports.RateLimitError = exports.ValidationError = exports.NotFoundError = exports.ApiError = exports.OwockibotError = void 0;
/**
 * Base class for all owockibot SDK errors
 */
class OwockibotError extends Error {
    constructor(message) {
        super(message);
        this.name = 'OwockibotError';
    }
}
exports.OwockibotError = OwockibotError;
/**
 * Represents an error response from the API
 */
class ApiError extends OwockibotError {
    constructor(message, status, code) {
        super(message);
        this.name = 'ApiError';
        this.status = status;
        this.code = code;
    }
}
exports.ApiError = ApiError;
/**
 * Error for 404 Not Found responses
 */
class NotFoundError extends ApiError {
    constructor(message = 'Resource not found', code) {
        super(message, 404, code);
        this.name = 'NotFoundError';
    }
}
exports.NotFoundError = NotFoundError;
/**
 * Error for 400 Bad Request / Validation errors
 */
class ValidationError extends ApiError {
    constructor(message = 'Validation failed', code) {
        super(message, 400, code);
        this.name = 'ValidationError';
    }
}
exports.ValidationError = ValidationError;
/**
 * Error for 429 Rate Limit Exceeded responses
 */
class RateLimitError extends ApiError {
    constructor(message = 'Rate limit exceeded', code) {
        super(message, 429, code);
        this.name = 'RateLimitError';
    }
}
exports.RateLimitError = RateLimitError;
/**
 * Error for 5xx Server errors
 */
class ServerError extends ApiError {
    constructor(message = 'Server error', status, code) {
        super(message, status || 500, code);
        this.name = 'ServerError';
    }
}
exports.ServerError = ServerError;
