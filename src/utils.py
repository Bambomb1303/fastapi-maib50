# utils.py
from collections import Counter

def get_difficulty_class(level_index: int) -> str:
    return ['basic', 'advanced', 'expert', 'master', 'remaster'][level_index] if 0 <= level_index < 5 else 'basic'

def get_fc_image(fc: int) -> str:
    return {
        3: 'UI_MSS_MBase_Icon_FC.png',
        2: 'UI_MSS_MBase_Icon_FCp.png',
        1: 'UI_MSS_MBase_Icon_AP.png',
        0: 'UI_MSS_MBase_Icon_APp.png'
    }.get(fc, '')

def get_fs_image(fs: int) -> str:
    return {
        0: 'UI_MSS_MBase_Icon_Sync.png',
        1: 'UI_MSS_MBase_Icon_FS.png',
        2: 'UI_MSS_MBase_Icon_FSp.png',
        3: 'UI_MSS_MBase_Icon_FSD.png',
        4: 'UI_MSS_MBase_Icon_FSDp.png'
    }.get(fs, '')

def get_dxstars(dx_score: int, total_dx_score: int) -> str:
    if total_dx_score == 0:
        return ''
    percentage = (dx_score / total_dx_score) * 100
    if percentage < 85:
        return ''
    elif percentage < 90:
        return "一星"
    elif percentage < 93:
        return "二星"
    elif percentage < 95:
        return "三星"
    elif percentage < 97:
        return "四星"
    else:
        return "五星"
    

def get_dxstars_image(dx_score: int, total_dx_score: int) -> str:
    if total_dx_score == 0:
        return ''
    percentage = (dx_score / total_dx_score) * 100
    if percentage < 85:
        return ''
    elif percentage < 90:
        return "UI_GAM_Gauge_DXScoreIcon_01.png"
    elif percentage < 93:
        return "UI_GAM_Gauge_DXScoreIcon_02.png"
    elif percentage < 95:
        return "UI_GAM_Gauge_DXScoreIcon_03.png"
    elif percentage < 97:
        return "UI_GAM_Gauge_DXScoreIcon_04.png"
    else:
        return "UI_GAM_Gauge_DXScoreIcon_05.png"

def get_rating_img(rating: int) -> str:
    thresholds = [15000, 14500, 14000, 13000, 12000, 10000, 7000, 4000, 2000, 1000, 0]
    filenames = [
        "UI_CMN_DXRating_11.png", "UI_CMN_DXRating_10.png", "UI_CMN_DXRating_09.png",
        "UI_CMN_DXRating_08.png", "UI_CMN_DXRating_07.png", "UI_CMN_DXRating_06.png",
        "UI_CMN_DXRating_05.png", "UI_CMN_DXRating_04.png", "UI_CMN_DXRating_03.png",
        "UI_CMN_DXRating_02.png", "UI_CMN_DXRating_01.png"
    ]
    for threshold, filename in zip(thresholds, filenames):
        if rating >= threshold:
            return filename
    return filenames[-1]

def pad_b50(scores_b35, scores_b15):
    scores_b35 = scores_b35[:35] + [{}] * (35 - len(scores_b35))
    scores_b15 = scores_b15[:15] + [{}] * (15 - len(scores_b15))
    return scores_b35, scores_b15

def calculate_counters(completion_type, music_data):
    fc_counter = Counter()
    fs_counter = Counter()
    rate_counter = Counter()

    for _, charts in music_data:
        for chart in charts:
            user_score = chart.get("user_score")
            if not user_score:
                continue

            val = user_score.get(completion_type)
            if val is None:
                continue

            if completion_type == "fc":
                fc_counter[val] += 1
            elif completion_type == "fs":
                fs_counter[val] += 1
            else:
                rate_counter[val] += 1

    return fc_counter, fs_counter, rate_counter