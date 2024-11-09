import { integer, pgTable } from "drizzle-orm/pg-core";

export const example = pgTable("example", {
  id: integer().primaryKey(),
});
