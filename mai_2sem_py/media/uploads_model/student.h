#ifndef STUDENT_HPP_
#define STUDENT_HPP_

typedef enum {
	male,
	female
} Sex;

typedef struct Student_ {
	char lastName[50];
	char initials[2];
	int sex;
	unsigned int groupNumber;
	int maths;
    int physic;
} Student;

#endif // !STUDENT_HPP_
