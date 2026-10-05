# V17.4 strong backbone transfer

STATUS: COMPLETE
DECISION: INNOVATION_1_PAPER_READY
R_HSPE_FROZEN: TRUE
INNOVATION_1: PAPER_READY
COMPLEMENTARY_SIGNAL: SUPPORTED
TEST: COMPLETE
MAIN_TABLE_RANK: see06_MAIN_TABLE.md
NEXT_EXPECTED_STEP: retrieve results and decide scientific positioning; no automatic Innovation2.

Added parameters:75; overhead depends on host architecture, recorded per arm. NCN/NCNC backbone unchanged. Training/inference/feature-cache seconds and peak GPU memory in per-arm results and phase feature metadata.
Baseline reuse rejected because prior epochs100 differ from current5/10; epoch budget and final-checkpoint rule explicitly follow V17.4.
PhaseA and B compare identical initialization, official train sampler, per-epoch negatives, permutations and CUDA RNG trace within each host/seed.

Complementarity to NCNC is supported by the specified validation and test gates.

A EFFECTS:
{
  "cora": {
    "delta_ncn": {
      "mean": 0.03988368719825238,
      "std": 0.02124726204744548,
      "median": 0.05148381791867873,
      "min": 0.015361339125597784,
      "max": 0.05280590455048062,
      "per_seed": [
        0.05148381791867873,
        0.015361339125597784,
        0.05280590455048062
      ],
      "wins": 3
    },
    "delta_ncnc": {
      "mean": 0.0081426176533241,
      "std": 0.021146575046167744,
      "median": 0.001005182141363803,
      "min": -0.008511681104501512,
      "max": 0.031934351923110005,
      "per_seed": [
        0.001005182141363803,
        0.031934351923110005,
        -0.008511681104501512
      ],
      "wins": 2
    },
    "delta_null": {
      "mean": 0.00522670536237498,
      "std": 0.01586340279455596,
      "median": 0.001005182141363803,
      "min": -0.008098905803557988,
      "max": 0.022773839749319125,
      "per_seed": [
        0.001005182141363803,
        0.022773839749319125,
        -0.008098905803557988
      ],
      "wins": 2
    }
  },
  "pubmed": {
    "delta_ncn": {
      "mean": 0.006716944454521275,
      "std": 0.00640838686815227,
      "median": 0.0032689908366800857,
      "min": 0.0027707242528594023,
      "max": 0.014111118274024337,
      "per_seed": [
        0.0032689908366800857,
        0.0027707242528594023,
        0.014111118274024337
      ],
      "wins": 3
    },
    "delta_ncnc": {
      "mean": 0.023022569254518694,
      "std": 0.01091811732061349,
      "median": 0.01801475950844178,
      "min": 0.015506660407382356,
      "max": 0.03554628784773195,
      "per_seed": [
        0.015506660407382356,
        0.01801475950844178,
        0.03554628784773195
      ],
      "wins": 3
    },
    "delta_null": {
      "mean": 0.022260493300655788,
      "std": 0.012607836684108958,
      "median": 0.01762546143186927,
      "min": 0.012626235076596104,
      "max": 0.03652978339350199,
      "per_seed": [
        0.01762546143186927,
        0.012626235076596104,
        0.03652978339350199
      ],
      "wins": 3
    }
  }
}
A GATES:
{
  "cora": {
    "nc_nc_pass": true,
    "null_pass": true,
    "initialization_negative_and_rng_match": true,
    "pass": true
  },
  "pubmed": {
    "nc_nc_pass": true,
    "null_pass": true,
    "initialization_negative_and_rng_match": true,
    "pass": true
  }
}

B EFFECTS:
{
  "cora": {
    "delta_ncn": {
      "mean": 0.016661857133345892,
      "std": 0.010558888932444499,
      "median": 0.0177581116912362,
      "min": 0.004491067656466896,
      "max": 0.027719382930745162,
      "per_seed": [
        0.026007428417403666,
        0.004491067656466896,
        0.007333294970877535,
        0.027719382930745162,
        0.0177581116912362
      ],
      "wins": 5
    },
    "delta_ncnc": {
      "mean": 0.027898317676625827,
      "std": 0.019283240422943687,
      "median": 0.026432150499090756,
      "min": 0.005023372439557416,
      "max": 0.05687686682710158,
      "per_seed": [
        0.026432150499090756,
        0.018114632515773277,
        0.05687686682710158,
        0.005023372439557416,
        0.03304456610160611
      ],
      "wins": 5
    },
    "delta_null": {
      "mean": 0.028873387224044644,
      "std": 0.02220736560771343,
      "median": 0.02477358554431275,
      "min": 0.003112039159402835,
      "max": 0.06352998306920643,
      "per_seed": [
        0.02477358554431275,
        0.020165547938976736,
        0.06352998306920643,
        0.003112039159402835,
        0.03278578040832447
      ],
      "wins": 5
    }
  },
  "pubmed": {
    "delta_ncn": {
      "mean": 0.0010027329533615291,
      "std": 0.0030582818326729618,
      "median": 0.00024390807273666493,
      "min": -0.0021384639263267724,
      "max": 0.005517256114586533,
      "per_seed": [
        -0.0021384639263267724,
        0.002484293684654748,
        0.00024390807273666493,
        -0.0010933291788435273,
        0.005517256114586533
      ],
      "wins": 3
    },
    "delta_ncnc": {
      "mean": 0.007023188654506374,
      "std": 0.004448729880943733,
      "median": 0.008815413677778161,
      "min": 0.002196344569990738,
      "max": 0.012278622150012186,
      "per_seed": [
        0.009272000562614457,
        0.002196344569990738,
        0.012278622150012186,
        0.002553562312136326,
        0.008815413677778161
      ],
      "wins": 5
    },
    "delta_null": {
      "mean": 0.006685298005243823,
      "std": 0.0039878207765349305,
      "median": 0.00805936817895303,
      "min": 0.0018510871398956796,
      "max": 0.011425698248803018,
      "per_seed": [
        0.00805936817895303,
        0.003300877071183872,
        0.011425698248803018,
        0.0018510871398956796,
        0.008789459387383514
      ],
      "wins": 5
    }
  }
}
B GATES:
{
  "cora": {
    "nc_nc_pass": true,
    "null_pass": true,
    "initialization_negative_and_rng_match": true,
    "pass": true
  },
  "pubmed": {
    "nc_nc_pass": true,
    "null_pass": true,
    "initialization_negative_and_rng_match": true,
    "pass": true
  }
}

third EFFECTS:
{
  "citeseer": {
    "delta_ncnc": {
      "mean": -0.02737937803369254,
      "std": 0.010627857325904716,
      "median": -0.03143486469477641,
      "min": -0.035382393512737975,
      "max": -0.015320875893563235,
      "per_seed": [
        -0.03143486469477641,
        -0.035382393512737975,
        -0.015320875893563235
      ],
      "wins": 0
    },
    "delta_null": {
      "mean": -0.03293616360796969,
      "std": 0.0227568848374444,
      "median": -0.04053546795837537,
      "min": -0.0509209953042552,
      "max": -0.007352027561278507,
      "per_seed": [
        -0.0509209953042552,
        -0.04053546795837537,
        -0.007352027561278507
      ],
      "wins": 0
    }
  }
}
third GATES:
{
  "citeseer": {
    "nc_nc_pass": false,
    "null_pass": false,
    "initialization_negative_and_rng_match": true,
    "pass": false
  }
}

TEST EFFECTS:
{
  "cora": {
    "delta_ncnc": {
      "mean": 0.025852682660934833,
      "std": 0.017824982388446015,
      "median": 0.03415585230049967,
      "min": 0.004307620484090946,
      "max": 0.04460612223645277,
      "per_seed": [
        0.03415585230049967,
        0.00947876706889994,
        0.04460612223645277,
        0.004307620484090946,
        0.03671505121473084
      ],
      "wins": 5
    },
    "delta_null": {
      "mean": 0.02798820251752021,
      "std": 0.019141083038670837,
      "median": 0.03432863265492614,
      "min": 0.006223738837590753,
      "max": 0.05220696921449164,
      "per_seed": [
        0.03432863265492614,
        0.010815684668793235,
        0.05220696921449164,
        0.006223738837590753,
        0.03636598721179929
      ],
      "wins": 5
    },
    "delta_ncn": {
      "mean": 0.016941774771170048,
      "std": 0.005785170230476603,
      "median": 0.018560811421342693,
      "min": 0.007129473384077767,
      "max": 0.021221746064083336,
      "per_seed": [
        0.02101917055176339,
        0.007129473384077767,
        0.016777672434583057,
        0.018560811421342693,
        0.021221746064083336
      ],
      "wins": 5
    }
  },
  "pubmed": {
    "delta_ncnc": {
      "mean": 0.007136914679784767,
      "std": 0.0025269652422456415,
      "median": 0.007610820161587428,
      "min": 0.004126349921137917,
      "max": 0.009854526052066714,
      "per_seed": [
        0.007610820161587428,
        0.004942591754414916,
        0.00915028550971686,
        0.004126349921137917,
        0.009854526052066714
      ],
      "wins": 5
    },
    "delta_null": {
      "mean": 0.007204156528389394,
      "std": 0.00464968619091962,
      "median": 0.006713329039592653,
      "min": 0.0022414465047587706,
      "max": 0.012355957820759378,
      "per_seed": [
        0.006713329039592653,
        0.003170389327880274,
        0.011539659948955894,
        0.0022414465047587706,
        0.012355957820759378
      ],
      "wins": 5
    },
    "delta_ncn": {
      "mean": 0.006361893990869061,
      "std": 0.004199333796861386,
      "median": 0.007418718841327165,
      "min": 0.0018130091178374386,
      "max": 0.010707554921924989,
      "per_seed": [
        0.0018130091178374386,
        0.007418718841327165,
        0.009774318641647128,
        0.002095868431608583,
        0.010707554921924989
      ],
      "wins": 5
    }
  }
}

DETAILS:
{
  "flags": [
    "STRONG_BACKBONE_TRANSFER_CONFIRMED",
    "BACKBONE_INDEPENDENT_TRANSFER_SUPPORTED",
    "THIRD_DATASET_TRANSFER_FAIL"
  ],
  "test_accessed": true
}
