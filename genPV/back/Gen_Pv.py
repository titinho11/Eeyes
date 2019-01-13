from Classes import SE, BV, PV
import random
import os


def gen_original_pv(bureau_vote):
    """
    This function generates the original PV for the Vote Bureau in parameter
    :param bureau_vote:
    :return: nothing is returned
    """
    global template_result
    pv = PV('AUTHENTIC', bureau_vote, template_result.copy())
    rest = bureau_vote.voters_num
    for candidate in pv.result:
        if candidate == 'NULL':
            continue
        voice = random.randint(0, rest)
        pv.result[candidate] = voice
        rest = rest - voice
    pv.result['NULL'] = rest
    bureau_vote.pVs.append(pv)


def gen_candidates_pvs_normal(bureau_vote):
    """
    This function generates the PVs of all the candidates in a vote bureau.
    This is neither with cheating nor error, meaning that every one has the same PV as the original
    :param bureau_vote:
    :return: nothing is returned
    """
    global session_electorale
    global probabilite
    for candidate in session_electorale.candidates:
        if random.random() <= probabilite:
            copy_original_pv = PV(candidate, bureau_vote, bureau_vote.pVs[0].result.copy())
            bureau_vote.pVs.append(copy_original_pv)
    copy_original_pv = PV(session_electorale.organism, bureau_vote, bureau_vote.pVs[0].result.copy())
    bureau_vote.pVs.append(copy_original_pv)


def gen_candidate_wrong_pv(candidate, bureau_vote):
    global template_result
    pv = PV(candidate, bureau_vote, template_result.copy())
    condition = True
    while condition:
        rest = bureau_vote.voters_num
        for can in pv.result:
            if can == 'NULL':
                continue
            voice = random.randint(0, rest)
            pv.result[can] = voice
            rest = rest - voice
        pv.result['NULL'] = rest
        condition = not check_win_in_result(candidate, pv.result)
    bureau_vote.pVs.append(pv)


def check_win_in_result(candidate, result):
    for can in result:
        if result[can] > result[candidate]:
            return False
    return True


def gen_candidates_pvs_chaos(bureau_vote):
    """
    This function generates the PVs of all the candidates in a vote bureau.
    Here every one cheats with a certain probability
    If a candidate is a cheater, he cheats with of probability of 0.5
    :param bureau_vote:
    :return:
    """
    global session_electorale
    global cheat_candidates
    global probabilite
    for candidate in session_electorale.candidates:
        if random.random() <= probabilite:
            if cheat_candidates[candidate]:
                if random.random() < 0.5:
                    gen_candidate_wrong_pv(candidate, bureau_vote)
                    continue
            copy_original_pv = PV(candidate, bureau_vote, bureau_vote.pVs[0].result.copy())
            bureau_vote.pVs.append(copy_original_pv)

    if session_electorale.current_president in session_electorale.candidates:
        for pv in bureau_vote.pVs:
            if pv.owner == session_electorale.current_president:
                copy_current_presi_pv = PV(session_electorale.organism, bureau_vote, pv.result.copy())
                bureau_vote.pVs.append(copy_current_presi_pv)
                break
    else:
        copy_original_pv = PV(session_electorale.organism, bureau_vote, bureau_vote.pVs[0].result.copy())
        bureau_vote.pVs.append(copy_original_pv)


def gen_candidates_pvs_fraude(bureau_vote):
    """
    This function generates the PVs of all the candidates in a vote bureau.
    Here the current president cheats with the organism
    :param bureau_vote:
    :return:
    """
    global session_electorale
    global probabilite
    for candidate in session_electorale.candidates:
        if random.random() <= probabilite:
            if candidate == session_electorale.current_president:
                if random.random() < 0.5:
                    gen_candidate_wrong_pv(candidate, bureau_vote)
                    continue
            copy_original_pv = PV(candidate, bureau_vote, bureau_vote.pVs[0].result.copy())
            bureau_vote.pVs.append(copy_original_pv)
    for pv in bureau_vote.pVs:
        if pv.owner == session_electorale.current_president:
            copy_current_presi_pv = PV(session_electorale.organism, bureau_vote, pv.result.copy())
            bureau_vote.pVs.append(copy_current_presi_pv)
            break


def gen_candidates_pvs_coalition(bureau_vote, type_coalition):
    global coalition_members
    global session_electorale
    global probabilite

    coalition_result = bureau_vote.pVs[0].result.copy()
    retreive_from_others = {}
    sum_retreives = 0
    #gen pv for candidates not in the coalition
    for candidate in session_electorale.candidates:
        if random.random() <= probabilite:
            if candidate not in coalition_members:
                copy_original_pv = PV(candidate, bureau_vote, bureau_vote.pVs[0].result.copy())
                bureau_vote.pVs.append(copy_original_pv)
                retreive_from_others[candidate] = random.randint(0,copy_original_pv.result[candidate])
                sum_retreives += retreive_from_others[candidate]
    #print(retreive_from_others)
    #gen pv for candidates in the coalition
    if type_coalition == 'equilibre':
        part = int(sum_retreives/len(coalition_members))
        for candidate in session_electorale.candidates:
            if random.random() <= probabilite:
                if candidate in coalition_members:
                    coalition_result[candidate] += part
                else:
                    coalition_result[candidate] -= retreive_from_others[candidate]
        coalition_result[coalition_members[0]] += sum_retreives-part*len(coalition_members)

        for member in coalition_members:
            pv = PV(member, bureau_vote, coalition_result.copy())
            bureau_vote.pVs.append(pv)

    elif type_coalition == 'concentre':
        if session_electorale.current_president in coalition_members:
            boss = session_electorale.current_president
        else:
            boss = random.choice(coalition_members)

        for candidate in session_electorale.candidates:
            if random.random() <= probabilite:
                if not candidate in coalition_members:
                    coalition_result[candidate] -= retreive_from_others[candidate]
                elif candidate == boss:
                    coalition_result[candidate] += sum_retreives

        for member in coalition_members:
            pv = PV(member, bureau_vote, coalition_result.copy())
            bureau_vote.pVs.append(pv)

    #gen pv for the organism
    if session_electorale.current_president in session_electorale.candidates:
        for pv in bureau_vote.pVs:
            if pv.owner == session_electorale.current_president:
                copy_current_presi_pv = PV(session_electorale.organism, bureau_vote, pv.result.copy())
                bureau_vote.pVs.append(copy_current_presi_pv)
                break
    else:
        copy_original_pv = PV(session_electorale.organism, bureau_vote, bureau_vote.pVs[0].result.copy())
        bureau_vote.pVs.append(copy_original_pv)


def gen_all_candidates_pvs(type_generation, type_coalition):
    """

    :param type_generation: can be 'normal' or 'chaos' or 'fraude' or 'coalition'
    :return:
    """
    global list_bureau_vote
    global session_electorale

    if type_generation == 'normal':
        for bv in list_bureau_vote:
            gen_candidates_pvs_normal(bv)
    elif type_generation == 'chaos':
        global cheat_candidates
        for candidate in session_electorale.candidates:
            if random.random() < 0.5:
                cheat_candidates[candidate] = False
            else:
                cheat_candidates[candidate] = True
        #print(cheat_candidates)
        for bv in list_bureau_vote:
            gen_candidates_pvs_chaos(bv)
    elif type_generation == 'fraude':
        for bv in list_bureau_vote:
            gen_candidates_pvs_fraude(bv)
    elif type_generation == 'coalition':
        global coalition_members
        coalition_members = random.sample(session_electorale.candidates, random.randint(2, len(session_electorale.candidates)))
        #print(coalition_members)
        for bv in list_bureau_vote:
            gen_candidates_pvs_coalition(bv, type_coalition)


def main(json_file, location_files, type_generation='normal', type_coalition = None, probabilite_possesion = 1):
    """

    :param json_file:
    :param type_generation: si 'normal' alors tous pv seront égaux aux originaux
    si 'chaos' alors chacun triche à sa guise
    si 'fraude' alors forcément le président courant se représente et il triche à sa guise avec l'organisme
    si 'coalition' alors il y'a un groupe de candidats qui triche
    :param type_coalition: il existe si type_generation vaut 'coalition'
    il peut prendre soit 'equilibre' soit 'concentre'
    :return:
    """
    global session_electorale
    session_electorale = SE(json_file)
    global cheat_candidates
    cheat_candidates = {}

    global template_result
    template_result = {}
    for candidate in session_electorale.candidates:
        template_result[candidate] = 0
    template_result['NULL'] = 0

    global list_bureau_vote
    list_bureau_vote = []

    global coalition_members
    coalition_members = []

    for node in session_electorale.list_nodes:
        if isinstance(node, BV):
            gen_original_pv(node)
            list_bureau_vote.append(node)

    global probabilite
    probabilite = probabilite_possesion
    gen_all_candidates_pvs(type_generation, type_coalition)

    os.makedirs('{}/Images'.format(location_files))
    os.makedirs('{}/.Jsons'.format(location_files))
    for candidate in session_electorale.candidates:
        os.makedirs('{}/Images/{}'.format(location_files, candidate.replace(' ','_')))
        os.makedirs('{}/.Jsons/{}'.format(location_files, candidate.replace(' ','_')))
    os.makedirs('{}/Images/{}'.format(location_files, session_electorale.organism))
    os.makedirs('{}/.Jsons/{}'.format(location_files, session_electorale.organism))
    os.makedirs('{}/Images/AUTHENTIC'.format(location_files))
    os.makedirs('{}/.Jsons/AUTHENTIC'.format(location_files))

    return list_bureau_vote