// > deno run --allow-read --allow-write scripts/merge.ts
import {
  find,
  unionBy,
  orderBy,
} from "https://deno.land/x/lodash@4.17.15-es/lodash.js";
import type { CourseItem, CoursePack, CourseDoc } from "./types";

const oldData = JSON.parse(Deno.readTextFileSync("./data.json"));
const newData = JSON.parse(Deno.readTextFileSync("./data_new.json"));

const uniqCourseNames: string[] = Array.from(
  new Set([...oldData, ...newData].map((item) => item.course_name)),
).sort();
const courseMap: Map<string, string[]> = new Map(
  uniqCourseNames.map((courseName) => [courseName, []]),
);
const merged: CourseItem[] = [];

for (const courseName of uniqCourseNames) {
  const oldPacks: CoursePack = find(oldData, [
    "course_name",
    courseName,
  ])?.packs;
  const newPacks: CoursePack = find(newData, [
    "course_name",
    courseName,
  ])?.packs;
  const mergedPacks: CoursePack[] = orderBy(
    unionBy(newPacks, oldPacks, "year"),
    ["year"],
    ["desc"],
  );

  merged.push({ course_name: courseName, packs: mergedPacks });
  courseMap.set(
    courseName,
    mergedPacks.map((pack) => pack.year),
  );
}

Deno.writeTextFileSync("./data.json", JSON.stringify(merged, undefined, 2));
Deno.writeTextFileSync(
  "./data_list.json",
  JSON.stringify(Array.from(courseMap.entries()), undefined, 2),
);
