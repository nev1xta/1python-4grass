#include "student.h"
#include <stdio.h>
#include <stdlib.h>

void usage() { printf("Usage: <program name> <out file name>"); }

int readStudent(Student *stud) {
  int res = scanf("%s %s %d %u %d %d\n"
			, stud->lastName
			, stud->initials
			, (int *)&stud->sex
			, &stud->groupNumber
			, &stud->maths
			, &stud->physic);
        printf("DEBUG(%d):%s\t%s\t%d\t%u\t%d\t%d\n"
            , res
			, stud->lastName
			, stud->initials
			, stud->sex
			, stud->groupNumber
			, stud->maths
			, stud->physic);
	return res == 6;
}

int main(int argc, char *argw[]) {
  if (argc < 2) {
    usage();
    return 1;
  }

  FILE *fileOut = fopen(argw[1], "wb");

	if (!fileOut) {
		printf("Error: can't open file\n");
		return 1;
	}
	
	Student stud;
	while (readStudent(&stud)) {
		fwrite(&stud, sizeof(Student), 1, fileOut);
	}

	fclose(fileOut);
  return 0;
}