-- For Cloudflare Hyperdrive:
-- CREATE ROLE hyperdrive_user LOGIN PASSWORD 'sufficientlyRandomPassword';
-- -- Here, you are granting it the postgres role. In practice, you want to create a role with lesser privileges.
-- GRANT postgres to hyperdrive_user;
CREATE TABLE IF NOT EXISTS "example" ("id" integer PRIMARY KEY NOT NULL);