#include <stdio.h>
#include <unistd.h>

float readValue(char* line, char* field)
{
	printf("*** readValue ***\n");
	printf("Line = %s", line);
	printf("Search for value of: %s\n", field);

	return 1.23111;
}

int main(int argc, char **argv) {
	char* line;
	ssize_t read = 0;
	size_t len = 0;

	while(read != -1)
	{
		read = getline(&line, &len, stdin);

		printf("*** main ***\n");
		printf("Line = %s]", line);

		float timeHour   = readValue(line, (char*)"hour");
		float timeMinute = readValue(line, (char*)"minute");
		float timeSec    = readValue(line, (char*)"sec");

		printf("Time = %f,%f,%f\n", timeHour, timeMinute, timeSec);
	}

//	free(line);

	return 0;
}


