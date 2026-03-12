#ifndef UNITY_H
#define UNITY_H

#include <stdbool.h>
#include <stdio.h>

#define UNITY_BEGIN() 0
#define UNITY_END() 0

#define TEST_ASSERT_TRUE(condition) do { if (!(condition)) { fprintf(stderr, "Test failed: %s\n", #condition); exit(1); } } while(0)
#define TEST_ASSERT_FALSE(condition) do { if (condition) { fprintf(stderr, "Test failed: %s\n", #condition); exit(1); } } while(0)
#define TEST_ASSERT_EQUAL(expected, actual) do { if ((expected) != (actual)) { fprintf(stderr, "Test failed: %s == %s\n", #expected, #actual); exit(1); } } while(0)

#define RUN_TEST(test_func) do { printf("Running %s...\n", #test_func); test_func(); printf("PASSED\n"); } while(0)

#endif
