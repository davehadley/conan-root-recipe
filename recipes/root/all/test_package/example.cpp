#define CATCH_CONFIG_MAIN 
#include <catch2/catch.hpp>

#include <iostream>
#include "TH1F.h"
#include "TFile.h"
#include "TTree.h"
#include "TTreeReader.h"
#include "Event.hpp"

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

void create_events_file(std::string name = "testevents.root", const int Nevent = 10, const int Npart = 10) {
    auto tfile = TFile::Open(name.c_str(), "RECREATE");
    auto tree = new TTree("tree", "tree");
    Event* event = 0;
    tree->Branch("events", &event);
    for(int eventnum = 0; eventnum < Nevent; ++eventnum) {
        event = new Event();
        for (int id = 0; id < Npart; ++id) {
            event->particles.push_back(Particle(id, {1.0, 2.0, 3.0, 4.0}));
        }
        tree->Fill();
        delete event;
        event = 0;
    }
    tree->Write();
    tfile->Close();
    delete tfile;
}

TEST_CASE( "Read/Write Events to File", "[tree]" ) {
    const std::string fname = "testevents.root";
    const int Nevent = 10;
    const int Npart = 10;
    create_events_file(fname, Nevent, Npart);
    auto tfile = TFile::Open(fname.c_str(), "READ");
    TTreeReader reader("tree", tfile);
    TTreeReaderValue<Event> event(reader, "events");
    REQUIRE(reader.GetEntries() == Nevent);
    bool didloop = false;
    while(reader.Next()) {
        didloop = true;
        REQUIRE(event.GetSetupStatus()==0);
        auto ev = (*event);
        REQUIRE(ev->particles.size() == Npart);
        for(int index = 0; index < Npart; ++index) {
            auto& p = ev->particles.at(index);
            REQUIRE(p.getID() == index);
            REQUIRE(p.getP4().X() == 1.0);
            REQUIRE(p.getP4().Y() == 2.0);
            REQUIRE(p.getP4().Z() == 3.0);
            REQUIRE(p.getP4().T() == 6.0);
        }
    }
    REQUIRE(didloop);
}


