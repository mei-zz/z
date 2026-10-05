#include <stdio.h>
#include <string.h>

int main(void) {
    FILE *f = fopen(".env", "r");
    char line[4096];
    if (!f) return 1;
    while (fgets(line, sizeof(line), f)) {
        if (strncmp(line, "psw=", 4) == 0) {
            char *value = line + 4;
            size_t n = strlen(value);
            while (n > 0 && (value[n - 1] == '\n' || value[n - 1] == '\r')) value[--n] = '\0';
            if (n >= 2 && ((value[0] == '"' && value[n - 1] == '"') || (value[0] == '\'' && value[n - 1] == '\''))) {
                value[n - 1] = '\0';
                value++;
            }
            fputs(value, stdout);
            fclose(f);
            return 0;
        }
    }
    fclose(f);
    return 1;
}
