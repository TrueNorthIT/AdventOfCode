#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

typedef struct {
    long long start;
    long long end;
} Interval;

int getline(char **lineptr, size_t *cap, FILE *stream) {
    if (lineptr == NULL || cap == NULL || stream == NULL) return -1;
    if (*lineptr == NULL || *cap == 0) {
        *cap = 128;
        *lineptr = (char *)malloc(*cap);
        if (*lineptr == NULL) return -1;
    }
    size_t len = 0;
    int ch;
    while ((ch = fgetc(stream)) != EOF) {
        if (len + 1 >= *cap) {
            size_t new_cap = (*cap) * 2;
            char *new_buf = (char *)realloc(*lineptr, new_cap);
            if (!new_buf) return -1;
            *lineptr = new_buf;
            *cap = new_cap;
        }
        (*lineptr)[len++] = (char)ch;
        if (ch == '\n')
            break;
    }
    if (len == 0 && ch == EOF) {
        return -1;
    }
    (*lineptr)[len] = '\0';
    return (int)len;
}

int compare_intervals(const void *a, const void *b) {
    const Interval *ia = (const Interval *)a;
    const Interval *ib = (const Interval *)b;
    if (ia->start < ib->start) return -1;
    if (ia->start > ib->start) return 1;
    if (ia->end   < ib->end)   return -1;
    if (ia->end   > ib->end)   return 1;
    return 0;
}

char *trim(char *s) {
    char *end;
    while (isspace((unsigned char)*s)) s++;
    if (*s == '\0') return s;
    end = s + strlen(s) - 1;
    while (end > s && isspace((unsigned char)*end)) end--;
    *(end + 1) = '\0';
    return s;
}

int main(void) {
    FILE *file = fopen("values.txt", "r");
    if (!file) {
        perror("Failed to open values.txt");
        return 1;
    }
    Interval *intervals = NULL;
    size_t count = 0, capacity = 0;
    char *line = NULL;
    size_t line_cap = 0;
    for (;;) {
        int len = getline(&line, &line_cap, file);
        if (len < 0) {
            break;
        }
        char *dash = strchr(line, '-');
        if (!dash) {
            break;
        }
        *dash = '\0';
        char *left  = trim(line);
        char *right = trim(dash + 1);
        if (*left == '\0' || *right == '\0') {
            continue;
        }
        char *endptr1, *endptr2;
        long long start = strtoll(left,  &endptr1, 10);
        long long end   = strtoll(right, &endptr2, 10);
        if (*endptr1 != '\0' || *endptr2 != '\0') {
            continue;
        }
        if (count == capacity) {
            size_t new_cap = (capacity == 0) ? 16 : capacity * 2;
            Interval *tmp = (Interval *)realloc(intervals, new_cap * sizeof(Interval));
            if (!tmp) {
                perror("realloc failed");
                free(intervals);
                free(line);
                fclose(file);
                return 1;
            }
            intervals = tmp;
            capacity  = new_cap;
        }
        intervals[count].start = start;
        intervals[count].end   = end;
        count++;
    }
    fclose(file);
    free(line);
    if (count == 0) {
        printf("0\n");
        free(intervals);
        return 0;
    }
    qsort(intervals, count, sizeof(Interval), compare_intervals);
    long long merged_total = 0;
    long long cur_start = intervals[0].start;
    long long cur_end   = intervals[0].end;
    for (size_t i = 1; i < count; i++) {
        long long start = intervals[i].start;
        long long end   = intervals[i].end;
        if (start > cur_end + 1) {
            merged_total += (cur_end - cur_start + 1);
            cur_start = start;
            cur_end   = end;
        } else {
            if (end > cur_end) cur_end = end;
        }
    }
    merged_total += (cur_end - cur_start + 1);
    printf("%lld\n", merged_total);
    free(intervals);
    return 0;
}