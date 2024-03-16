// > deno run --allow-read --allow-write scripts/format.ts
import {
  find,
  unionBy,
  orderBy,
} from "https://deno.land/x/lodash@4.17.15-es/lodash.js";

const data = JSON.parse(Deno.readTextFileSync("./data.json"));

const uniqCourseNames = Array.from(
  new Set<string>(data.map((item) => item.course_name)),
).sort();

const sorted: { course_name: string; packs: any[] }[] = [];

for (const courseName of uniqCourseNames) {
  const packs = find(data, ["course_name", courseName])?.packs;

  sorted.push({
    course_name: courseName,
    packs: orderBy(unionBy(packs, "year"), ["year"], ["desc"]),
  });
}

Deno.writeTextFileSync("./data.json", JSON.stringify(sorted, undefined, 2));
