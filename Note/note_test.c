
#include <stdarg.h>
#include <stddef.h>
#include <setjmp.h>
#include <stdint.h>
#include <cmocka.h>
/* A test case that does nothing and succeeds. */
extern int add(int ,int );
extern void add_note();
void test_add(){
    assert_int_equal(add(3,3),6);
}
void test_add_note(){
    add_note();
}
static void null_test_success(void **state) {
    (void) state; /* unused */
}

int main(void) {
    const struct CMUnitTest tests[] = {
        cmocka_unit_test(null_test_success),
        cmocka_unit_test(add_note),
        cmocka_unit_test(test_add),
    };

    return cmocka_run_group_tests(tests, NULL, NULL);
}
