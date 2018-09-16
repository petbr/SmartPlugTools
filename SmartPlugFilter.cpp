#include <stdio.h>
#include <string.h>

// "current":0.032122,
// readValue "current" => 0.032122
// Line = ('Received: ', '{"emeter":{"get_realtime":{"current":0.031207,"voltage":236.398535,"power":2.478820,"total":2.274000,"err_code":0}}}')
bool readValue(char* line, char* field, float* value)
{
	int fieldSize = strlen(field);
	printf("*** readValue ***\n");
	printf("Line = %s", line);
	printf("Search for value of: %s\n", field);
	printf("Size of field = %d\n", fieldSize);

	bool bRes = false; // Until found OK

	char* resFieldValue = strstr(line, field) + fieldSize+2;
	if( resFieldValue != NULL)
	{
		char* commaStr = strstr(resFieldValue, ",");

		printf("res      = %s", resFieldValue);
		printf("commaStr = %s", commaStr);

		bRes = true;
	}

	return bRes;
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

		bool  bRes;
		float timeHour, timeMinute, timeSec;
		float power;
		bRes = readValue(line, (char*)"hour",   &timeHour);
		bRes = readValue(line, (char*)"minute", &timeMinute);
		bRes = readValue(line, (char*)"sec",    &timeSec);
		bRes = readValue(line, (char*)"power",  &power);

		printf("Time = %f,%f,%f\n", timeHour, timeMinute, timeSec);
		printf("Power = %f\n", power);
		printf("Peter was here!\n");
	}

//	free(line);

	return 0;
}


