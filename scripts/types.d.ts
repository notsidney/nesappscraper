export type CourseItem = {
  course_name: string;
  packs: CoursePack[];
};

export type CoursePack = {
  year: string;
  link: string;
  docs: CourseDoc[];
};

export type CourseDoc = {
  doc_name: string;
  doc_link: string;
};
