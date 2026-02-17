"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ServerError = exports.RateLimitError = exports.ValidationError = exports.NotFoundError = exports.ApiError = exports.OwockibotClient = void 0;
// Main client export
const client_1 = require("./client");
Object.defineProperty(exports, "OwockibotClient", { enumerable: true, get: function () { return client_1.OwockibotClient; } });
// Type exports
var types_1 = require("./types");
Object.defineProperty(exports, "ApiError", { enumerable: true, get: function () { return types_1.ApiError; } });
Object.defineProperty(exports, "NotFoundError", { enumerable: true, get: function () { return types_1.NotFoundError; } });
Object.defineProperty(exports, "ValidationError", { enumerable: true, get: function () { return types_1.ValidationError; } });
Object.defineProperty(exports, "RateLimitError", { enumerable: true, get: function () { return types_1.RateLimitError; } });
Object.defineProperty(exports, "ServerError", { enumerable: true, get: function () { return types_1.ServerError; } });
// Re-export for convenience
exports.default = client_1.OwockibotClient;
