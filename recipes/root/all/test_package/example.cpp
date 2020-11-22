#define CATCH_CONFIG_MAIN 
#include <catch2/catch.hpp>

#include <iostream>
#include "TH1F.h"

TEST_CASE( "Basic histogram operation", "[hist]" ) {
    int N = 100;
    TH1F hist(
        "testhist",
        "This is a test",
        100,
        -5.0,
        5.0
    );
    hist.FillRandom("gaus", N);
    int actual = hist.GetEntries();
    REQUIRE(N == actual);
}

