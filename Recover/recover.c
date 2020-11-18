// Recover images from a forensic file (memory card)

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define BLOCK 512

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check if the user has input a valid command-line
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // Remember input file
    char *infile = argv[1];

    // Open input file
    FILE *inptr = fopen(infile, "r");

    // Check if the infile was correctly opened
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s\n", infile);
        return 2;
    }

    // Create outfile pointer
    FILE *outptr = NULL;

    // Create buffer
    BYTE buffer[BLOCK];

    // Create outfile
    char outfile[8];

    // Keep track of the name of JPEGs created
    int jpg_counter = 0;

    // Keep track that the first JPEG exists
    bool jpg_exists = false;

    while (fread(buffer, sizeof(buffer), 1, inptr) == 1)
    {
        // Signaling for when a new jpg needs to be written
        bool write_new = false;

        // Already found a JPEG?
        if (jpg_exists)
        {
            if (buffer[0] == 0xff &&
                buffer[1] == 0xd8 &&
                buffer[2] == 0xff &&
                (buffer[3] & 0xf0) == 0xe0)
            {
                // Counter for every time a new JPEG image is found
                jpg_counter++;
                write_new = true;

                // Close that file
                fclose(outptr);
            }

            // Start of a new JPEG?
            if (write_new)
            {
                // Name output file
                sprintf(outfile, "%03d.jpg", jpg_counter);

                // Open file for writing
                outptr = fopen(outfile, "w");
            }
            else
            {
                // Close file
                fclose(outptr);

                // Open file to write 512 bytes until new JPEG is found
                outptr = fopen(outfile, "a");
            }
            // Write to outfile
            fwrite(buffer, 512, 1, outptr);
        }
        // When the start of the 1st JPEG is found
        if (buffer[0] == 0xff &&
            buffer[1] == 0xd8 &&
            buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0 && jpg_exists == false)
        {
            jpg_exists = true;
            // Name output file
            sprintf(outfile, "%03d.jpg", jpg_counter);

            // Open img file for writing
            outptr = fopen(outfile, "w");

            // Write to outfile
            fwrite(buffer, 512, 1, outptr);
        }
    }

    // Close any remaining files
    fclose(outptr);
    fclose(inptr);

    // Success
    return 0;
}
