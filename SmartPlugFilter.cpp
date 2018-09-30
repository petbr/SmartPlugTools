#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// "current":0.032122,
// readValue "current" => 0.032122
// Line = ('Received: ', '{"emeter":{"get_realtime":{"current":0.031207,"voltage":236.398535,"power":2.478820,"total":2.274000,"err_code":0}}}')
bool readValue(char* line, char* field, float* pValue)
{
	int fieldSize = strlen(field);

	printf("*** readValue ***\n");
	printf("Line = %s", line);
	printf("Search for value of: [%s]\n", field);
	printf("Size of field = %d\n", fieldSize);

	bool bRes = false; // Until found OK

	char* sField = strstr(line, field);
	printf("sField = %s\n", sField);
	if( sField != NULL)
	{
		char* sCommaAfterField = strstr(sField, ",");

		if(sCommaAfterField == NULL)
		{
			// If no "," is found...then the end character is "}"
			sCommaAfterField = strstr(sField, "}");
		}
		// ....."power":2.478820,"total"
		//       sField
		//              sFieldValue
		//                      sCommaAfterField
		char* sFieldValue = sField + fieldSize + strlen("\":");
		int   valueSize   = sCommaAfterField - sFieldValue;

		char sFieldValueOnly[20];
		strncpy(sFieldValueOnly, sFieldValue, valueSize);
		sFieldValueOnly[valueSize] = '\0';

		*pValue = atof(sFieldValueOnly);

		printf("sField           = %s", sField);
		printf("sCommaAfterField = %s", sCommaAfterField);
		printf("sFieldValue      = %s", sFieldValue);
		printf("valueSize        = %d\n", valueSize);
		printf("sFieldValueOnly  = %s\n", sFieldValueOnly);
		printf("value            = %f\n", *pValue);


		bRes = true;
	}

	return bRes;
}

int main(int argc, char **argv) {
	char* line;
	ssize_t read = 0;
	size_t len = 0;

	for (int i=0; i<argc; i++)
	{
		printf("arg[%d] = %s\n", i, argv[i]);
	}

	char* fieldToSearchFor = argv[1];
	printf("What to search for: %s\n", fieldToSearchFor);

	while(read != -1)
	{
		read = getline(&line, &len, stdin);

		printf("*** main ***\n");
		printf("Line = %s", line);

		bool  bRes;
		float timeHour, timeMinute, timeSec;
		float power;
		bRes = readValue(line, (char*)"hour",   &timeHour);
		bRes = readValue(line, (char*)"min", &timeMinute);
		bRes = readValue(line, (char*)"sec",    &timeSec);
		bRes = readValue(line, (char*)"power",  &power);

		printf("Time = %f,%f,%f\n", timeHour, timeMinute, timeSec);
		printf("Power = %f\n", power);
		printf("Peter was here!\n");
	}

//	free(line);

	return 0;
}


