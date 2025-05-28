#include "student.h"
#include <stdio.h>
#include <stdlib.h>

void usage() { printf("Usage: <program name> <number of Students> <output file name>\n"); }

void generateStudent(Student *stud) {
	stud->lastName[0] = 'A' + rand() % 26;
  int lastNameLen = 5 + rand() % 10;
	for (int i = 1; i < lastNameLen + 1; ++i) {
    stud->lastName[i] = 'a' + rand() % 26;
  }
	stud->initials[0] = 'A' + rand()%26;
	stud->initials[1] = 'A' + rand()%26;
	
	stud->sex = rand() % 2;
	stud->groupNumber = 1 + rand() % 10;
	stud->maths = rand() % 6;
	stud->physic = rand() % 6;
}

int main(int argc, char *argw[]) {
  if (argc < 3) {
    usage();
    return 1;
  }
  int n = atoi(argw[1]);
	FILE * fileOut = fopen(argw[2], "w");

	Student stud;
  for (int i = 0; i < n; ++i) {
		generateStudent(&stud);
		fprintf(fileOut, "%50s %2s %d %u %d %d\n", stud.lastName, stud.initials, (int)stud.sex, stud.groupNumber, (int)stud.maths, (int)stud.physic);
  }

  return 0;
}
