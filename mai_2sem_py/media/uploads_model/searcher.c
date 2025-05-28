#include "student.h"
#include <stdio.h>
#include <stdlib.h>

void usage() { printf("Usage: <program name> -f <fileDB> -p <class number>"); }

int parseFlag(int flagN, int argc, char *argw[], const char **fileDB,
              const char **classNumberS) {
  if (argw[flagN][0] != '-') {
    usage();
    return 0;
  }
  if (argw[flagN][1] == 'f') {
    *fileDB = argw[flagN + 1];
  } else if (argw[flagN][1] == 'p') {
    *classNumberS = argw[flagN + 1];
  } else {
    usage();
    return 0;
  }
  return 1;
}

int main(int argc, char *argw[]) {
  if (argc < 5) {
    usage();
    return 1;
  }
  const char *fileDB, *classNumberS;
	for (int i = 0; i < argc; ++i) {
		printf("%d) %s\n", i, argw[i]);
	}

  if (!parseFlag(1, argc, argw, &fileDB, &classNumberS) ||
      !parseFlag(3, argc, argw, &fileDB, &classNumberS)) {
    return 1;
  }

  int pClassNumber = atoi(classNumberS);
  FILE *fileIn = fopen(fileDB, "rb");
	if (!fileIn) {
		printf("Error: can't open file\n");
    usage();
    return 1;
	}
  Student abit;
  int cnt = 0;
  while (fread(&abit, sizeof(Student), 1, fileIn) == 1) {

    if ((abit.groupNumber == pClassNumber) && (abit.maths >= 4 && abit.physic >= 4)) {
      cnt++;

    }
  }
  printf("%d", cnt);
}