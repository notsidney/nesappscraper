// > deno run --allow-read --allow-write merge.ts
import {
	find,
	unionBy,
	orderBy,
} from "https://deno.land/x/lodash@4.17.15-es/lodash.js";

const oldData = JSON.parse(Deno.readTextFileSync("./data_old.json"));
const newData = JSON.parse(Deno.readTextFileSync("./data_new.json"));

const uniqCourseNames = Array.from(
	new Set([...oldData, ...newData].map((item) => item.course_name))
).sort();

const merged = [];

for (const courseName of uniqCourseNames) {
	const oldPacks = find(oldData, ["course_name", courseName])?.packs;
	const newPacks = find(newData, ["course_name", courseName])?.packs;

	merged.push({
		course_name: courseName,
		packs: orderBy(unionBy(newPacks, oldPacks, "year"), ["year"], ["desc"]),
	});
}

Deno.writeTextFileSync("./data.json", JSON.stringify(merged, undefined, 2));
