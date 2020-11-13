#include <iostream>
#include "TH1F.h"

int main() {
    TH1F hist(
        "testhist",
        "This is a test",
        100,
        -5.0,
        5.0
    );
    hist.FillRandom("gaus", 100);
}
