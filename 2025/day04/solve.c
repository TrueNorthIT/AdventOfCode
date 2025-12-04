#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#define EXIT_SUCCESS 0
#define EXIT_ARG_ERROR 1
#define EXIT_FILE_ERROR 2

typedef struct __Coord
{
    int x;
    int y;
} coord;

typedef struct __Map
{
    char **map;
    int height;
    int width;
} map;

char *read_line(FILE *f)
{
    size_t size = 256;
    char *buf = malloc(size);
    if (!buf) return NULL;

    size_t len = 0;

    while (fgets(buf + len, size - len, f)) {
        len = strlen(buf);
        if (len > 0 && buf[len - 1] == '\n')
            return buf;
        size *= 2;
        char *tmp = realloc(buf, size);
        if (!tmp) {
            free(buf);
            return NULL;
        }
        buf = tmp;
    }
    if (len > 0) return buf;
    free(buf);
    return NULL;
}

int get_height(char *filename)
{
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error: Could not find or open the file.\n");
        exit(EXIT_FILE_ERROR);
    }
    int map_height = 0;
    char *line;
    while ((line = read_line(file)) != NULL) {
        map_height++;
        free(line);
    }
    fclose(file);
    return map_height;
}

int get_width(char *filename)
{
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error: Could not find or open the file.\n");
        exit(EXIT_FILE_ERROR);
    }
    char *line = read_line(file);
    int map_width = 0;

    if (line) {
        size_t len = strlen(line);
        while (len > 0 && (line[len - 1] == '\n' || line[len - 1] == '\r'))
            len--;
        map_width = (int)len;
        free(line);
    }
    fclose(file);
    return map_width;
}

void create_map(map *this, char *filename)
{
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error: Could not find or open the file.\n");
        exit(EXIT_FILE_ERROR);
    }
    this->map = malloc(this->height * sizeof(char *));
    if (!this->map) {
        perror("malloc");
        exit(EXIT_FILE_ERROR);
    }
    for (int i = 0; i < this->height; i++) {
        this->map[i] = malloc(this->width * sizeof(char));
        if (!this->map[i]) {
            perror("malloc");
            exit(EXIT_FILE_ERROR);
        }
    }
    for (int i = 0; i < this->height; i++) {
        char *line = read_line(file);

        if (!line) {
            for (int j = 0; j < this->width; j++) {
                this->map[i][j] = ' ';
            }
            continue;
        }
        size_t len = strlen(line);
        size_t L = 0;
        while (L < len &&
               line[L] != '\n' &&
               line[L] != '\r' &&
               L < (size_t)this->width) {
            this->map[i][L] = line[L];
            L++;
        }
        for (int j = (int)L; j < this->width; j++) {
            this->map[i][j] = ' ';
        }
        free(line);
    }
    fclose(file);
}

void free_map(map *this)
{
    if (!this || !this->map) return;
    for (int i = 0; i < this->height; i++) {
        free(this->map[i]);
    }
    free(this->map);
    this->map = NULL;
}

void print_map(map *this)
{
    printf("\n");
    for (int i = 0; i < this->height; i++) {
        for (int j = 0; j < this->width; j++) {
            printf("%c", this->map[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

int solve_map(map *this)
{
    int rolls_around = 0;
    int roll_accssessed = 0;
    int rolls_removed = 1;
    int max_rolls = 4;
    while (rolls_removed)
    {
        rolls_removed = 0;
        for (int line = 0; line < this->height; line++)
        {
            for (int character = 0; character < this->width; character++)
            {
                if (this->map[line][character] == '@')
                {
                    if (character - 1 >= 0 &&
                        this->map[line][character] == this->map[line][character - 1]) {
                        rolls_around += 1;
                    }
                    if (character + 1 < this->width &&
                        this->map[line][character] == this->map[line][character + 1]) {
                        rolls_around += 1;
                    }
                    if (line - 1 >= 0 &&
                        this->map[line][character] == this->map[line - 1][character]) {
                        rolls_around += 1;
                    }
                    if (line + 1 < this->height &&
                        this->map[line][character] == this->map[line + 1][character]) {
                        rolls_around += 1;
                    }
                    if (line - 1 >= 0 && character - 1 >= 0 &&
                        this->map[line][character] == this->map[line - 1][character - 1]) {
                        rolls_around += 1;
                    }
                    if (line - 1 >= 0 && character + 1 < this->width &&
                        this->map[line][character] == this->map[line - 1][character + 1]) {
                        rolls_around += 1;
                    }
                    if (line + 1 < this->height && character - 1 >= 0 &&
                        this->map[line][character] == this->map[line + 1][character - 1]) {
                        rolls_around += 1;
                    }
                    if (line + 1 < this->height && character + 1 < this->width &&
                        this->map[line][character] == this->map[line + 1][character + 1]) {
                        rolls_around += 1;
                    }

                    if (rolls_around < max_rolls) {
                        roll_accssessed += 1;
                        rolls_removed = 1;
                        this->map[line][character] = 'X';
                    }
                    rolls_around = 0;
                }
            }
        }
    }
    return roll_accssessed;
}

int main (int argc, char *argv[])
{
    if (argc != 2) {
        printf("Usage: %s <filename>\n", argv[0]);
        exit(EXIT_ARG_ERROR);
    }
    map *this_map = malloc(sizeof(map));
    if (!this_map) {
        perror("malloc");
        exit(EXIT_FILE_ERROR);
    }
    this_map->height = get_height(argv[1]);
    this_map->width  = get_width(argv[1]);
    create_map(this_map, argv[1]);
    int rolls = solve_map(this_map);
    print_map(this_map);
    printf("Removed rolls: %d\n", rolls);
    free_map(this_map);
    free(this_map);
    exit(EXIT_SUCCESS);
}