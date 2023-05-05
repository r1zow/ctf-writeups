#include <stdio.h>
#include <stdlib.h>
#include <cstdlib>

int main(int argc, char *argv[]) {
   int seed = atoi(argv[1]);
  // printf("Seed - %d\n", seed);
   srand(seed);
   for (int i = 1; i <= 7; ++i) {
        printf("%d\n", rand());
   }
}
