# Escola LMS aka Wellms Headless LMS 

Laravel Headless LMS REST API.

[![swagger](https://img.shields.io/badge/documentation-swagger-green)](https://api-docs.wellms.io)
[![phpunit](https://github.com/EscolaLMS/API/actions/workflows/phpunit-tests.yml/badge.svg)](https://github.com/EscolaLMS/API/actions/workflows/phpunit-tests.yml)
[![downloads](https://img.shields.io/packagist/dt/escolalms/api)](https://packagist.org/packages/escolalms/api)
[![downloads](https://img.shields.io/packagist/v/escolalms/api)](https://packagist.org/packages/escolalms/api)
[![downloads](https://img.shields.io/packagist/l/escolalms/api)](https://packagist.org/packages/escolalms/api)
[![Maintainability](https://api.codeclimate.com/v1/badges/68b4fbde49bcd465e482/maintainability)](https://codeclimate.com/github/EscolaLMS/API/maintainability)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FEscolaLMS%2FAPI.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FEscolaLMS%2FAPI?ref=badge_shield)
[![Known Vulnerabilities](https://snyk.io/test/github/EscolaLMS/API/badge.svg)](https://snyk.io/test/github/EscolaLMS/API)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=EscolaLMS_API&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=EscolaLMS_API)

## Documentation

Most of the documentation is hosted at [docs.wellms.io](https://docs.wellms.io/).

## Configuration

Please not that API is based on Laravel but it's configured by environmental variables
Please don't create or edit any `.env` file but use environmental variables with `LARAVEL_` prefix, see [docker-compose.yml](docker-compose.yml) for reference.

As we want this package to be stateless and easy to scale all configuration is stored either in database or in environmental variables.

See [docs][docs] for more details.

Application is designed to be stateless - it is controlled by [environmental variables](docs/enviromental-variables.md)

## Installation from source code

If you want to use the software consider using our docker images or using [Create-LMS-App/](https://github.com/EscolaLMS/Create-LMS-App/) helper.

You should consider install with our [installation package](https://docs.wellms.io/getting-started/guide.html).

To install default docker environment either clone this repo or use

See [docs/multidomain.md][docs/multidomain.md] for more details how to quick start.

### Quick start

1. Clone this repo
2. `docker compose up -d`
3. Run `make init` to initialize the database and generate API documentation
4. Access the Swagger API documentation at [http://api.localhost/api/documentation](http://api.localhost/api/documentation)

## Demo

[https://api-stage.escolalms.com/api/documentation](https://api-stage.escolalms.com/api/documentation)

This is fully working demo. **Note** that content is regenerated every day - it's a seeder that is not persistent, every day database and files are cleared and rebuilt from skratch.

## Packages

This API consists of Laravel and multiple packages.

List of all packages is available at [packagist.org/?query=escolalms](https://packagist.org/?query=escolalms).

## Tests

Just run `phpunit` to test all the packages.

Summary code coverage from all the packages:

[![cc](https://raw.githubusercontent.com/EscolaLMS/.github/main/api-tests/cc-badge.svg)](https://github.com/EscolaLMS/API/actions/workflows/phpunit-cc.yml)
[![Tests Code Coverage](https://github.com/EscolaLMS/API/actions/workflows/phpunit-cc.yml/badge.svg)](https://github.com/EscolaLMS/API/actions/workflows/phpunit-cc.yml)
[![cc](https://raw.githubusercontent.com/EscolaLMS/.github/main/api-tests/cc-tests.svg)](https://github.com/EscolaLMS/API/actions/workflows/phpunit-cc.yml)
[![cc](https://raw.githubusercontent.com/EscolaLMS/.github/main/api-tests/cc-assertions.svg)](https://github.com/EscolaLMS/API/actions/workflows/phpunit-cc.yml)

## Test

There are hundreds of tests in the packages and they are divided into:

### Integration packages test

Each packge contains their own php integration test this repo runs all of the

To run use `./vendor/bin/phpunit`

## Tasks

See [makefile](makefile) for all available devops tasks

## Logging and Monitoring

### Enhanced Logging System (v0.1)

The API now includes comprehensive logging capabilities for debugging and monitoring:

#### 1. **Caddy Access Logs**
- Full request/response logging with URLs, methods, and status codes
- View logs: `docker compose logs -f caddy`
- Shows complete request paths and response times

#### 2. **PHP-FPM Access Logs**
- Detailed FastCGI request metrics including memory and CPU usage
- Enhanced format showing request URI, response times, and resource consumption
- View logs: `docker compose logs -f api`

#### 3. **Laravel Application Logs**
- Custom middleware logs all incoming requests with headers and authentication details
- Daily rotating log files in `storage/logs/`
- View logs: `docker compose exec api tail -f storage/logs/laravel-$(date +%Y-%m-%d).log`

#### 4. **Environment Variables**
- `LARAVEL_LOG_CHANNEL=stderr` - Outputs Laravel logs to Docker logs
- `LARAVEL_APP_LOG_LEVEL=debug` - Set to debug for maximum verbosity

### Viewing Logs

```bash
# All containers
docker compose logs -f

# Specific service logs
docker compose logs -f api      # API and PHP-FPM logs
docker compose logs -f caddy    # Web server access logs
docker compose logs -f postgres # Database logs
docker compose logs -f redis    # Cache logs

# Laravel application logs
docker compose exec api tail -f storage/logs/laravel-$(date +%Y-%m-%d).log

# Filter logs by severity
docker compose logs -f 2>&1 | grep -E "(ERROR|WARNING)"
```

### Default Credentials

For testing and development:
- **Email:** admin@escolalms.com
- **Password:** secret

Access API documentation at: http://api.localhost/api/documentation

### Database Management

Access the database through Adminer web interface:
- **URL:** http://localhost:8078
- **System:** PostgreSQL
- **Server:** postgres
- **Username:** default
- **Password:** secret
- **Database:** default

## License

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FEscolaLMS%2FAPI.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2FEscolaLMS%2FAPI?ref=badge_large)
