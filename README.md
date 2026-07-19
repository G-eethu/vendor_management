# Vendor Management

A custom ERPNext/Frappe application for managing vendor onboarding requests with validations, approval workflow, automatic supplier creation, REST APIs, reporting, and automated tests.

## Setup Instructions

1. Get the app.
   ```bash
   bench get-app <repository_url>
   ```

2. Install the app.
   ```bash
   bench --site <site_name> install-app vendor_management
   ```

3. Run migrations.
   ```bash
   bench --site <site_name> migrate
   ```

## Assumptions

- Email is mandatory.
- GST Number is optional but must be valid if provided.
- Annual Turnover cannot be negative.
- Supplier is created only after the request is approved.
- Duplicate suppliers are prevented using GST Number or Supplier Name.

## API Documentation

- **Create Vendor Request**
  - `POST /api/method/vendor_management.api.api.create_request`

- **Get Vendor Request**
  - `GET /api/method/vendor_management.api.api.get_request?name=<request_name>`

## Design Decisions

- Business validations are implemented in the DocType controller.
- Supplier creation is automated after approval.
- Duplicate supplier creation is prevented by checking existing records.
- A Script Report summarizes requests grouped by Vendor Type.

## License

MIT