COG_QUOTAS = ((1, 1, 1, 1, 1, 1, 1, 1), (5, 5, 5, 5, 5, 5, 5, 5))
COG_UNSEEN = 1
COG_BATTLED = 2
COG_DEFEATED = 3
COG_COMPLETE1 = 4
COG_COMPLETE2 = 5


def get_min_cog_quota(av) -> int:
    return 1


def get_max_cog_quota(av) -> int:
    return av.slotData.get('maxed_cog_gallery_quota', 5)
