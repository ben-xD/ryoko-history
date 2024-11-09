import { drizzle, NodePgDatabase } from "drizzle-orm/node-postgres";
import * as schema from "./schema/index.js";

export const connectToDb = (databaseUrl: string, logDatabase: boolean) => {
  return drizzle(databaseUrl, {
    logger: logDatabase,
    schema,
  }) satisfies Database;
};

export type Database = NodePgDatabase<typeof schema>;
