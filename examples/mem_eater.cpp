#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

int main(int argc, char ** argv)
{
    static const int SIZE = 10000000;

    int size = 0;
    for (int i = 0; ; i++)
    {
        if (size < 1000000000)
        {
            void * mem = malloc(SIZE);
            if (mem == NULL)
            {
                fprintf(stderr, "Allocation failed\r\n");
            }
            else
            {
                size += SIZE;
                memset(mem, i, SIZE);
            }
        }

        sleep(1);
    }
}