"""Generate mock eye-tracking TSV files for 10 participants (P003–P012)."""
import random
import math
import os

random.seed(42)

# ── helpers ──────────────────────────────────────────────────────────────────

def rnd(lo, hi):
    return random.randint(lo, hi)

def rnd_f(lo, hi, dp=5):
    return round(random.uniform(lo, hi), dp)

def tab(*args):
    return "\t".join(str(a) for a in args)

# ── task / AOI definitions (same for all participants) ───────────────────────

TASKS = {
    "findDice":          {"duration": (8000, 12000),  "aois": ["answer", "M1","M2","M3","M4","M5","M6","M7"],                                 "aoi_sizes": {"answer":17504,"M1":4204,"M2":5305,"M3":8262,"M4":3696,"M5":3918,"M6":8320,"M7":11589}},
    "findYummy":         {"duration": (4000, 7000),   "aois": ["answer","aoi1","aoi2","aoi3","aoi4","aoi5","aoi6","aoi8","aoi9"],              "aoi_sizes": {"answer":4623,"aoi1":3174,"aoi2":1485,"aoi3":4445,"aoi4":839,"aoi5":6089,"aoi6":7803,"aoi8":1541,"aoi9":4355}},
    "frog":              {"duration": (14000, 18000),  "aois": ["answer","M1","M2","M3","M4","M5","M6","M7","M8","M9","M10","M11","M12","M13","M14","M15"], "aoi_sizes": {"answer":13923,"M1":9089,"M2":9423,"M3":16017,"M4":16626,"M5":11866,"M6":15260,"M7":11088,"M8":13281,"M9":10957,"M10":11583,"M11":13553,"M12":16098,"M13":14542,"M14":11974,"M15":9878}},
    "frogInBathroom":    {"duration": (18000, 24000),  "aois": ["answer1","M1","M2","M3","M4","M5","M6","M7","M8","M9","M10"],                "aoi_sizes": {"answer1":6472,"M1":9018,"M2":13253,"M3":16799,"M4":12926,"M5":22150,"M6":28124,"M7":12941,"M8":53218,"M9":55572,"M10":13005}},
    "headphoneInBathroom":{"duration": (5000, 9000),  "aois": ["answer","M1","M2","M3","M4","M5","M6","M7","M8"],                             "aoi_sizes": {"answer":11814,"M1":23117,"M2":19961,"M3":11678,"M4":56160,"M5":33704,"M6":4253,"M7":37920,"M8":16542}},
    "spotNeedleInst":    {"duration": (8000, 12000),  "aois": ["answer","M1","M2","M3","M4","M5","M6","M7","M8","M9"],                        "aoi_sizes": {"answer":3888,"M1":2533,"M2":11998,"M3":11168,"M4":10145,"M5":1293,"M6":698,"M7":1570,"M8":4167,"M9":2766}},
    "whoCheats":         {"duration": (8000, 14000),  "aois": ["answer","M1","M2","M3","M4","M5","M6","M7","M8","M9"],                        "aoi_sizes": {"answer":5000,"M1":4079,"M2":2107,"M3":2213,"M4":1306,"M5":1536,"M6":1650,"M7":4068,"M8":4827,"M9":3984}},
    "whoThief":          {"duration": (8000, 14000),  "aois": ["answer","M1","M2","M3","M4","M5","M6","M7","M8","M9","M10"],                  "aoi_sizes": {"answer":5200,"M1":1626,"M2":8141,"M3":5301,"M4":8827,"M5":3984,"M6":4068,"M7":4176,"M8":4827,"M9":3984,"M10":6854}},
}

ENTIRE_RECORDING_MEDIA = "EndTq,findDice,findYummy,frog,frogInBathroom,headphoneInBathroom,PracticeIns,spotNeedleInst,StartInst,Text (1),whoCheats,whoThief"

METRICS_HEADER = "\t".join([
    "Recording","Participant","Timeline","TOI","Interval","Media","AOI","AOI_size",
    "Duration_of_interval","Start_of_interval","Last_key_press",
    "Total_duration_of_fixations","Average_duration_of_fixations","Minimum_duration_of_fixations","Maximum_duration_of_fixations","Number_of_fixations",
    "Time_to_first_fixation","Duration_of_first_fixation","Last_AOI_viewed","AOI_at_interval_end",
    "Average_pupil_diameter","Average_eye_openness",
    "Total_duration_of_whole_fixations","Average_duration_of_whole_fixations","Minimum_duration_of_whole_fixations","Maximum_duration_of_whole_fixations","Number_of_whole_fixations","Time_to_first_whole_fixation","Duration_of_first_whole_fixation","Average_whole-fixation_pupil_diameter","Average_whole-fixation_eye_openness",
    "Total_duration_of_Visit","Average_duration_of_Visit","Minimum_duration_of_Visit","Maximum_duration_of_Visit","Number_of_Visits","Time_to_first_Visit","Duration_of_first_Visit",
    "Total_duration_of_Glances","Average_duration_of_Glances","Minimum_duration_of_Glances","Maximum_duration_of_Glances","Number_of_Glances","Time_to_first_Glance","Duration_of_first_Glance",
    "Number_of_mouse_clicks","Time_to_first_mouse_click","Time_from_first_fixation_to_mouse_click",
    "Number_of_mouse_clicks_and_releases","Time_to_first_mouse_click_and_release","Time_from_first_fixation_to_mouse_click_and_release",
    "Number_of_saccades_in_AOI","Time_to_entry_saccade","Time_to_exit_saccade","Peak_velocity_of_entry_saccade","Peak_velocity_of_exit_saccade"
])


def make_fix_block(duration, n_fix, ttf):
    """Return (total, avg, min, max, n) fixation stats."""
    if n_fix == 0:
        return 0, "", "", "", 0
    avg = duration // n_fix
    lo = max(100, avg - rnd(50, 150))
    hi = avg + rnd(50, 200)
    return duration, avg, lo, hi, n_fix


def metrics_row(rec, part, toi, media, aoi, aoi_size, dur, start_of_interval, last_key, hit_answer):
    """Generate one metrics row for a given AOI/participant."""
    is_answer = (aoi in ("answer", "answer1"))

    if hit_answer or (is_answer and random.random() < 0.4):
        n_fix = rnd(1, 5)
        ttf = rnd(500, min(dur - 300, 8000))
        total_fix = rnd(150, min(dur, 3500))
        avg_fix = total_fix // n_fix
        min_fix = max(100, avg_fix - rnd(50, 100))
        max_fix = avg_fix + rnd(50, 300)
        dur_first = rnd(100, 600)
        pd = rnd_f(2.5, 3.8)
        eo = rnd_f(8.0, 10.0)
        # whole fixations
        wf_total, wf_avg, wf_min, wf_max, wf_n = make_fix_block(total_fix, n_fix, ttf)
        # visits
        n_vis = rnd(1, n_fix)
        vis_total = total_fix + rnd(0, 200)
        vis_avg = vis_total // n_vis
        vis_min = max(100, vis_avg - 50)
        vis_max = vis_avg + rnd(50, 200)
        ttfvis = ttf - rnd(0, 50)
        dur_first_vis = dur_first + rnd(0, 50)
        # glances
        n_gl = n_vis
        gl_total = vis_total + rnd(0, 100)
        gl_avg = gl_total // n_gl
        gl_min = max(100, gl_avg - 50)
        gl_max = gl_avg + rnd(50, 150)
        ttfgl = ttfvis - rnd(0, 40)
        dur_first_gl = dur_first_vis + rnd(0, 30)
        # clicks
        n_click = 1 if (is_answer and random.random() < 0.7) else 0
        ttfc = rnd(ttf + 100, dur - 100) if n_click else ""
        ttfc_fix = (ttfc - ttf) if n_click else ""
        # saccades
        n_sacc = rnd(1, 3)
        t_entry = ttfgl - rnd(20, 60) if ttfgl > 60 else 0
        t_exit  = ttfgl + total_fix + rnd(10, 50)
        pv_entry = rnd_f(50, 400)
        pv_exit  = rnd_f(50, 400)

        last_aoi = aoi
        aoi_end  = aoi if random.random() < 0.6 else ""
    else:
        # no fixation on this AOI
        n_fix = 0; ttf = ""; total_fix = 0; avg_fix = ""; min_fix = ""; max_fix = ""; dur_first = ""
        pd = ""; eo = ""
        wf_total = 0; wf_avg = ""; wf_min = ""; wf_max = ""; wf_n = 0; ttfwf = ""; dur_first_wf = ""; pd_wf = ""; eo_wf = ""
        n_vis = 0; vis_total = 0; vis_avg = ""; vis_min = ""; vis_max = ""; ttfvis = ""; dur_first_vis = ""
        n_gl = 0; gl_total = 0; gl_avg = ""; gl_min = ""; gl_max = ""; ttfgl = ""; dur_first_gl = ""
        n_click = 0; ttfc = ""; ttfc_fix = ""
        n_sacc = 0; t_entry = ""; t_exit = ""; pv_entry = ""; pv_exit = ""
        last_aoi = ""; aoi_end = ""

        return tab(rec, part, "Timeline1", toi, 1, media, aoi, aoi_size,
                   dur, start_of_interval, last_key,
                   0,"","","",0,"","",last_aoi,aoi_end,
                   "","",
                   0,"","","",0,"","","","",
                   0,"","","",0,"","",
                   0,"","","",0,"","",
                   0,"","",0,"","",
                   0,"","","","")

    ttfwf = ttf
    dur_first_wf = dur_first
    pd_wf = pd
    eo_wf = eo

    return tab(rec, part, "Timeline1", toi, 1, media, aoi, aoi_size,
               dur, start_of_interval, last_key,
               total_fix, avg_fix, min_fix, max_fix, n_fix, ttf, dur_first, last_aoi, aoi_end,
               pd, eo,
               wf_total, wf_avg, wf_min, wf_max, wf_n, ttfwf, dur_first_wf, pd_wf, eo_wf,
               vis_total, vis_avg, vis_min, vis_max, n_vis, ttfvis, dur_first_vis,
               gl_total, gl_avg, gl_min, gl_max, n_gl, ttfgl, dur_first_gl,
               n_click, ttfc, ttfc_fix, n_click, ttfc, ttfc_fix,
               n_sacc, t_entry, t_exit, pv_entry, pv_exit)


def generate_metrics(participants):
    lines = [METRICS_HEADER]
    for idx, (rec_num, part) in enumerate(participants, start=5):
        rec = f"Recording{rec_num}"
        recording_start = rnd(150000, 200000)

        # cumulative start-of-interval offsets
        cumulative = 0
        task_offsets = {}
        for task_name, task_info in TASKS.items():
            task_offsets[task_name] = cumulative
            cumulative += rnd(*task_info["duration"])

        total_rec_dur = cumulative + rnd(5000, 15000)

        for task_name, task_info in TASKS.items():
            task_dur = rnd(*task_info["duration"])
            task_start = task_offsets[task_name] + recording_start
            answer_aoi = task_info["aois"][0]  # first aoi is always "answer" or "answer1"

            for aoi in task_info["aois"]:
                aoi_size = task_info["aoi_sizes"][aoi]
                hit = (aoi == answer_aoi)
                row = metrics_row(rec, part, task_name, task_name, aoi, aoi_size,
                                  task_dur, task_start, "Escape", hit)
                lines.append(row)

        # Entire Recording rows — one per task × per AOI (simplified: just answer AOIs)
        er_start = recording_start
        er_media = ENTIRE_RECORDING_MEDIA
        for task_name, task_info in TASKS.items():
            task_dur = rnd(*task_info["duration"])
            answer_aoi = task_info["aois"][0]
            aoi_size   = task_info["aoi_sizes"][answer_aoi]
            row = metrics_row(rec, part, "Entire Recording", er_media, answer_aoi,
                              aoi_size, total_rec_dur, 0, "Escape", True)
            lines.append(row)

    return "\n".join(lines)


# ── Data export ───────────────────────────────────────────────────────────────

DATAEXPORT_HEADER = "\t".join([
    "Recording timestamp","Computer timestamp","Sensor","Project name","Export date",
    "Participant name","Recording name","Recording date","Recording date UTC",
    "Recording start time","Recording start time UTC","Recording duration",
    "Timeline name","Recording Fixation filter name","Recording software version",
    "Recording resolution height","Recording resolution width","Recording monitor latency",
    "Average calibration accuracy (mm)","Average calibration precision SD (mm)",
    "Average calibration precision RMS (mm)","Average calibration accuracy (degrees)",
    "Average calibration precision SD (degrees)","Average calibration precision RMS (degrees)",
    "Average calibration accuracy (pixels)","Average calibration precision SD (pixels)",
    "Average calibration precision RMS (pixels)",
    "Average validation accuracy (mm)","Average validation precision SD (mm)",
    "Average validation precision RMS (mm)","Average validation accuracy (degrees)",
    "Average validation precision SD (degrees)","Average validation precision RMS (degrees)",
    "Average validation accuracy (pixels)","Average validation precision SD (pixels)",
    "Average validation precision RMS (pixels)",
    # AOI sizes
    "AOI size [findYummy - answer]","AOI size [headphoneInBathroom - answer]",
    "AOI size [findDice - answer]","AOI size [frog - answer]","AOI size [spotNeedleInst - answer]",
    "AOI size [whoCheats - answer]","AOI size [whoThief - answer]","AOI size [frogInBathroom - answer1]",
    "AOI size [findYummy - aoi1]","AOI size [findYummy - aoi2]","AOI size [findYummy - aoi3]",
    "AOI size [findYummy - aoi4]","AOI size [findYummy - aoi5]","AOI size [findYummy - aoi6]",
    "AOI size [findYummy - aoi8]","AOI size [findYummy - aoi9]",
    "AOI size [frogInBathroom - M1]","AOI size [headphoneInBathroom - M1]","AOI size [findDice - M1]",
    "AOI size [frog - M1]","AOI size [spotNeedleInst - M1]","AOI size [whoCheats - M1]","AOI size [whoThief - M1]",
    "AOI size [frogInBathroom - M2]","AOI size [headphoneInBathroom - M2]","AOI size [findDice - M2]",
    "AOI size [frog - M2]","AOI size [spotNeedleInst - M2]","AOI size [whoCheats - M2]","AOI size [whoThief - M2]",
    "AOI size [frogInBathroom - M3]","AOI size [headphoneInBathroom - M3]","AOI size [findDice - M3]",
    "AOI size [frog - M3]","AOI size [spotNeedleInst - M3]","AOI size [whoCheats - M3]","AOI size [whoThief - M3]",
    "AOI size [frogInBathroom - M4]","AOI size [headphoneInBathroom - M4]","AOI size [findDice - M4]",
    "AOI size [frog - M4]","AOI size [spotNeedleInst - M4]","AOI size [whoCheats - M4]","AOI size [whoThief - M4]",
    "AOI size [frogInBathroom - M5]","AOI size [headphoneInBathroom - M5]","AOI size [findDice - M5]",
    "AOI size [frog - M5]","AOI size [spotNeedleInst - M5]","AOI size [whoCheats - M5]","AOI size [whoThief - M5]",
    "AOI size [frogInBathroom - M6]","AOI size [headphoneInBathroom - M6]","AOI size [findDice - M6]",
    "AOI size [frog - M6]","AOI size [spotNeedleInst - M6]","AOI size [whoCheats - M6]","AOI size [whoThief - M6]",
    "AOI size [frogInBathroom - M7]","AOI size [headphoneInBathroom - M7]","AOI size [findDice - M7]",
    "AOI size [frog - M7]","AOI size [spotNeedleInst - M7]","AOI size [whoCheats - M7]","AOI size [whoThief - M7]",
    "AOI size [frogInBathroom - M8]","AOI size [headphoneInBathroom - M8]",
    "AOI size [frog - M8]","AOI size [spotNeedleInst - M8]","AOI size [whoCheats - M8]","AOI size [whoThief - M8]",
    "AOI size [frogInBathroom - M9]",
    "AOI size [frog - M9]","AOI size [spotNeedleInst - M9]","AOI size [whoCheats - M9]","AOI size [whoThief - M9]",
    "AOI size [frogInBathroom - M10]","AOI size [frog - M10]","AOI size [whoThief - M10]",
    "AOI size [frog - M11]","AOI size [frog - M12]","AOI size [frog - M13]","AOI size [frog - M14]","AOI size [frog - M15]",
    # time-series columns
    "Eyetracker timestamp","Event","Event value",
    "Gaze point X","Gaze point Y","Gaze point left X","Gaze point left Y",
    "Gaze point right X","Gaze point right Y",
    "Gaze direction left X","Gaze direction left Y","Gaze direction left Z",
    "Gaze direction right X","Gaze direction right Y","Gaze direction right Z",
    "Pupil diameter left","Pupil diameter right","Pupil diameter filtered",
    "Eye openness left","Eye openness right","Eye openness filtered",
    "Validity left","Validity right",
    "Eye position left X (DACSmm)","Eye position left Y (DACSmm)","Eye position left Z (DACSmm)",
    "Eye position right X (DACSmm)","Eye position right Y (DACSmm)","Eye position right Z (DACSmm)",
    "Gaze point left X (DACSmm)","Gaze point left Y (DACSmm)",
    "Gaze point right X (DACSmm)","Gaze point right Y (DACSmm)",
    "Gaze point X (MCSnorm)","Gaze point Y (MCSnorm)",
    "Gaze point left X (MCSnorm)","Gaze point left Y (MCSnorm)",
    "Gaze point right X (MCSnorm)","Gaze point right Y (MCSnorm)",
    "Presented Stimulus name","Presented Media name",
    "Presented Media width","Presented Media height",
    "Presented Media position X (DACSpx)","Presented Media position Y (DACSpx)",
    "Original Media width","Original Media height",
    "Eye movement type","Eye movement event duration","Eye movement type index",
    "Fixation point X","Fixation point Y","Fixation point X (MCSnorm)","Fixation point Y (MCSnorm)",
    "Ungrouped",
    # AOI hits (176-259)
    "AOI hit [findYummy - answer]","AOI hit [headphoneInBathroom - answer]",
    "AOI hit [findDice - answer]","AOI hit [frog - answer]","AOI hit [spotNeedleInst - answer]",
    "AOI hit [whoCheats - answer]","AOI hit [whoThief - answer]","AOI hit [frogInBathroom - answer1]",
    "AOI hit [findYummy - aoi1]","AOI hit [findYummy - aoi2]","AOI hit [findYummy - aoi3]",
    "AOI hit [findYummy - aoi4]","AOI hit [findYummy - aoi5]","AOI hit [findYummy - aoi6]",
    "AOI hit [findYummy - aoi8]","AOI hit [findYummy - aoi9]",
    "AOI hit [frogInBathroom - M1]","AOI hit [headphoneInBathroom - M1]","AOI hit [findDice - M1]",
    "AOI hit [frog - M1]","AOI hit [spotNeedleInst - M1]","AOI hit [whoCheats - M1]","AOI hit [whoThief - M1]",
    "AOI hit [frogInBathroom - M2]","AOI hit [headphoneInBathroom - M2]","AOI hit [findDice - M2]",
    "AOI hit [frog - M2]","AOI hit [spotNeedleInst - M2]","AOI hit [whoCheats - M2]","AOI hit [whoThief - M2]",
    "AOI hit [frogInBathroom - M3]","AOI hit [headphoneInBathroom - M3]","AOI hit [findDice - M3]",
    "AOI hit [frog - M3]","AOI hit [spotNeedleInst - M3]","AOI hit [whoCheats - M3]","AOI hit [whoThief - M3]",
    "AOI hit [frogInBathroom - M4]","AOI hit [headphoneInBathroom - M4]","AOI hit [findDice - M4]",
    "AOI hit [frog - M4]","AOI hit [spotNeedleInst - M4]","AOI hit [whoCheats - M4]","AOI hit [whoThief - M4]",
    "AOI hit [frogInBathroom - M5]","AOI hit [headphoneInBathroom - M5]","AOI hit [findDice - M5]",
    "AOI hit [frog - M5]","AOI hit [spotNeedleInst - M5]","AOI hit [whoCheats - M5]","AOI hit [whoThief - M5]",
    "AOI hit [frogInBathroom - M6]","AOI hit [headphoneInBathroom - M6]","AOI hit [findDice - M6]",
    "AOI hit [frog - M6]","AOI hit [spotNeedleInst - M6]","AOI hit [whoCheats - M6]","AOI hit [whoThief - M6]",
    "AOI hit [frogInBathroom - M7]","AOI hit [headphoneInBathroom - M7]","AOI hit [findDice - M7]",
    "AOI hit [frog - M7]","AOI hit [spotNeedleInst - M7]","AOI hit [whoCheats - M7]","AOI hit [whoThief - M7]",
    "AOI hit [frogInBathroom - M8]","AOI hit [headphoneInBathroom - M8]",
    "AOI hit [frog - M8]","AOI hit [spotNeedleInst - M8]","AOI hit [whoCheats - M8]","AOI hit [whoThief - M8]",
    "AOI hit [frogInBathroom - M9]",
    "AOI hit [frog - M9]","AOI hit [spotNeedleInst - M9]","AOI hit [whoCheats - M9]","AOI hit [whoThief - M9]",
    "AOI hit [frogInBathroom - M10]","AOI hit [frog - M10]","AOI hit [whoThief - M10]",
    "AOI hit [frog - M11]","AOI hit [frog - M12]","AOI hit [frog - M13]","AOI hit [frog - M14]","AOI hit [frog - M15]",
    "Client area position X (DACSpx)","Client area position Y (DACSpx)",
    "Viewport position X","Viewport position Y","Viewport width","Viewport height",
    "Full page width","Full page height","Mouse position X","Mouse position Y"
])

# constant AOI sizes (same as real data)
AOI_SIZES_FIXED = [
    4623,11814,17504,13923,3888,5000,5200,6472,
    3174,1485,4445,839,6089,7803,1541,4355,
    9018,23117,4204,9089,2533,4079,1626,
    13253,19961,5305,9423,11998,2107,8141,
    16799,11678,8262,16017,11168,2213,5301,
    12926,56160,3696,16626,10145,1306,8827,
    22150,33704,3918,11866,1293,1536,3984,
    28124,4253,8320,15260,698,1650,4068,
    12941,37920,11589,11088,1570,4176,4500,          # M7: frogInBath,hphone,findDice,frog,spotNeedle,whoCheats,whoThief
    53218,16542,13281,4167,4827,3800,                 # M8: frogInBath,hphone,frog,spotNeedle,whoCheats,whoThief
    55572,10957,2766,3984,4100,                       # M9: frogInBath,frog,spotNeedle,whoCheats,whoThief
    13005,11583,6854,
    13553,16098,14542,11974,9878
]
N_AOI_SIZE_COLS = len(AOI_SIZES_FIXED)  # 84

N_AOI_HIT_COLS = 84  # same count as AOI size cols

MEDIA_SEQUENCE = ["findDice","findYummy","frog","frogInBathroom","headphoneInBathroom","spotNeedleInst","whoCheats","whoThief"]
MEDIA_DIMS = {
    "findDice":           (1920, 1080, 1920, 1080),
    "findYummy":          (1920, 1080, 1920, 1080),
    "frog":               (1920, 1080, 1920, 1080),
    "frogInBathroom":     (1920, 1080, 1920, 1080),
    "headphoneInBathroom":(1920, 1080, 1920, 1080),
    "spotNeedleInst":     (1920, 1080, 1920, 1080),
    "whoCheats":          (1920, 1080, 1920, 1080),
    "whoThief":           (1920, 1080, 1920, 1080),
}

EYE_MOVEMENT_TYPES = ["EyesNotFound","Fixation","Saccade","Unclassified"]


def generate_data_export(participants, rows_per_participant=800):
    lines = [DATAEXPORT_HEADER]

    for rec_num, part in participants:
        rec_name = f"Recording{rec_num}"
        base_ts = rnd(9660000000000, 9680000000000)
        comp_ts = base_ts
        rec_date = "4/9/2026"
        start_time = f"0{rnd(8,10)}:{rnd(10,59):02d}:{rnd(0,59):02d}.000"
        rec_dur = rnd(140000, 160000)

        # calibration stats (per-participant constants)
        cal_mm = (rnd_f(0.3,0.9), rnd_f(0.1,0.4), rnd_f(0.1,0.4))
        cal_deg= (rnd_f(0.3,0.9), rnd_f(0.1,0.4), rnd_f(0.1,0.4))
        cal_px = (rnd_f(8,25),    rnd_f(3,12),     rnd_f(3,12))
        val_mm = (rnd_f(0.3,0.9), rnd_f(0.1,0.4), rnd_f(0.1,0.4))
        val_deg= (rnd_f(0.3,0.9), rnd_f(0.1,0.4), rnd_f(0.1,0.4))
        val_px = (rnd_f(8,25),    rnd_f(3,12),     rnd_f(3,12))

        meta_prefix = tab(
            0, comp_ts, "Eye Tracker",
            "VisualTask with recording", "4/10/2026",
            part, rec_name, rec_date, rec_date, start_time, start_time, rec_dur,
            "Timeline1", "Tobii I-VT (Fixation)", "24.21.435",
            1080, 1920, rnd(1,5),
            *cal_mm, *cal_deg, *cal_px, *val_mm, *val_deg, *val_px,
        )
        # AOI sizes (same for all rows of this participant)
        aoi_sizes_str = "\t".join(str(s) for s in AOI_SIZES_FIXED)

        # distribute rows evenly across media segments so all tasks are covered
        rows_per_media = rows_per_participant // len(MEDIA_SEQUENCE)
        media_row_map = []
        for m in MEDIA_SEQUENCE:
            media_row_map.extend([m] * rows_per_media)
        # fill remainder with last media
        while len(media_row_map) < rows_per_participant:
            media_row_map.append(MEDIA_SEQUENCE[-1])

        # time advances monotonically; reset per segment to stay within task duration
        eye_ts = 0
        seg_ts = 0
        current_media_idx = -1
        fix_x, fix_y = rnd(400, 1500), rnd(200, 900)
        em_type = "Fixation"
        em_dur = 0
        em_idx = 0

        for i in range(rows_per_participant):
            media = media_row_map[i]
            new_media_idx = MEDIA_SEQUENCE.index(media)
            if new_media_idx != current_media_idx:
                seg_ts = 0
                current_media_idx = new_media_idx
            seg_ts += rnd(8, 9)
            eye_ts += rnd(8, 9)
            rec_ts = eye_ts

            gx = rnd(200, 1720) if random.random() > 0.05 else ""
            gy = rnd(100,  980) if gx != "" else ""

            if gx != "":
                glx = gx + rnd(-15, 15); gly = gy + rnd(-10, 10)
                grx = gx + rnd(-15, 15); gry = gy + rnd(-10, 10)
                pd_l = rnd_f(2.5, 4.2); pd_r = rnd_f(2.5, 4.2)
                pd_f = round((pd_l + pd_r) / 2, 5)
                eo_l = rnd_f(7.5, 10.0); eo_r = rnd_f(7.5, 10.0)
                eo_f = round((eo_l + eo_r) / 2, 5)
                val_l = "Valid"; val_r = "Valid"
                ep_lx = rnd_f(-50, 50); ep_ly = rnd_f(-30, 30); ep_lz = rnd_f(480, 600)
                ep_rx = rnd_f(-50, 50); ep_ry = rnd_f(-30, 30); ep_rz = rnd_f(480, 600)
                gp_lx = rnd_f(-30, 30); gp_ly = rnd_f(-20, 20)
                gp_rx = rnd_f(-30, 30); gp_ry = rnd_f(-20, 20)
                gx_norm = round(gx / 1920, 5); gy_norm = round(gy / 1080, 5)
                glx_norm = round(glx/1920, 5); gly_norm = round(gly/1080, 5)
                grx_norm = round(grx/1920, 5); gry_norm = round(gry/1080, 5)
                # eye movement
                if random.random() < 0.05:
                    em_type = random.choice(EYE_MOVEMENT_TYPES)
                    em_idx += 1
                    fix_x = gx; fix_y = gy
                    em_dur = rnd(100, 800)
                em_type_val = em_type
                fx = fix_x; fy = fix_y
                fx_norm = round(fx/1920, 5); fy_norm = round(fy/1080, 5)
                # AOI hits: randomly assign 0 or 1; answer AOI has higher chance
                aoi_hits = [random.choices([0,1], weights=[7,3])[0] for _ in range(N_AOI_HIT_COLS)]
                aoi_hits_str = "\t".join(str(h) for h in aoi_hits)
                # gaze direction
                gd_lx = rnd_f(-0.3, 0.3); gd_ly = rnd_f(-0.3, 0.3); gd_lz = rnd_f(0.85, 1.0)
                gd_rx = rnd_f(-0.3, 0.3); gd_ry = rnd_f(-0.3, 0.3); gd_rz = rnd_f(0.85, 1.0)
            else:
                glx=gly=grx=gry=""
                pd_l=pd_r=pd_f=""
                eo_l=eo_r=eo_f=""
                val_l=val_r="Invalid"
                ep_lx=ep_ly=ep_lz=ep_rx=ep_ry=ep_rz=""
                gp_lx=gp_ly=gp_rx=gp_ry=""
                gx_norm=gy_norm=glx_norm=gly_norm=grx_norm=gry_norm=""
                gd_lx=gd_ly=gd_lz=gd_rx=gd_ry=gd_rz=""
                em_type_val="EyesNotFound"; em_dur=""; em_idx_val=em_idx
                fx=fy=fx_norm=fy_norm=""
                aoi_hits_str = "\t".join([""] * N_AOI_HIT_COLS)

            med_info = MEDIA_DIMS.get(media, (1920,1080,1920,1080))

            row = tab(
                rec_ts, comp_ts + eye_ts*1000, "Eye Tracker",
                "VisualTask with recording", "4/10/2026",
                part, rec_name, rec_date, rec_date, start_time, start_time, rec_dur,
                "Timeline1", "Tobii I-VT (Fixation)", "24.21.435",
                1080, 1920, rnd(1,5),
                *cal_mm, *cal_deg, *cal_px, *val_mm, *val_deg, *val_px,
                aoi_sizes_str,
                eye_ts, "", "",
                gx, gy, glx, gly, grx, gry,
                gd_lx, gd_ly, gd_lz, gd_rx, gd_ry, gd_rz,
                pd_l, pd_r, pd_f, eo_l, eo_r, eo_f,
                val_l, val_r,
                ep_lx, ep_ly, ep_lz, ep_rx, ep_ry, ep_rz,
                gp_lx, gp_ly, gp_rx, gp_ry,
                gx_norm, gy_norm, glx_norm, gly_norm, grx_norm, gry_norm,
                media, media,
                med_info[0], med_info[1], 0, 0, med_info[2], med_info[3],
                em_type_val, em_dur, em_idx,
                fx, fy, fx_norm, fy_norm,
                "",
                aoi_hits_str,
                960, 540, 0, 0, 1920, 1080, 1920, 1080,
                rnd(200, 1720), rnd(100, 980)
            )
            lines.append(row)

    return "\n".join(lines)


# ── main ─────────────────────────────────────────────────────────────────────

participants = [(i, f"P{i-2:03d}") for i in range(5, 15)]  # Recording5..14, P003..P012

print("Generating mock Metrics TSV...")
metrics_content = generate_metrics(participants)
out_metrics = os.path.join(os.path.dirname(__file__), "..", "data", "raw",
                            "mock_VisualTask_Metrics.tsv")
with open(out_metrics, "w", encoding="utf-8") as f:
    f.write(metrics_content)
print(f"  Written: {out_metrics}  ({metrics_content.count(chr(10))+1} rows)")

print("Generating mock Data export TSV (~800 rows/participant)...")
export_content = generate_data_export(participants, rows_per_participant=800)
out_export = os.path.join(os.path.dirname(__file__), "..", "data", "raw",
                           "mock_VisualTask_Data_export.tsv")
with open(out_export, "w", encoding="utf-8") as f:
    f.write(export_content)
print(f"  Written: {out_export}  ({export_content.count(chr(10))+1} rows)")
print("Done.")
