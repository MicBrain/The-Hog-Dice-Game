"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

# Taking turns

def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    ans=0
    checker = False
    while num_rolls>0:
        temp = dice()
        if temp == 1:
            checker = True
        ans = ans + temp
        num_rolls=num_rolls-1
    if checker == True:
        return 1
    else:
        return ans

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    if num_rolls == 0:
        return max(opponent_score//10, opponent_score%10) +1
    else:
        return roll_dice(num_rolls, dice)

# Playing a game

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    if (score + opponent_score)%7 == 0: 
        return four_sided
    else:
        return six_sided

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    score, opponent_score = 0, 0
    while score<goal and opponent_score<goal:
        p0= strategy0(score, opponent_score) 
        if select_dice(score, opponent_score) == four_sided: 
            dice = four_sided
        else:
            dice = six_sided
        current_score0 = take_turn(p0, opponent_score, dice)
        score = score+current_score0
        if score == opponent_score* 2 or opponent_score == 2 * score:
            score, opponent_score = opponent_score, score
        if score >=100:
            return score, opponent_score
        p1 = strategy1(opponent_score, score)
        if select_dice(score, opponent_score) == four_sided: 
            dice = four_sided
        else:
            dice = six_sided 
        current_score1 = take_turn(p1, score, dice)
        opponent_score = opponent_score + current_score1
        if score == opponent_score* 2 or opponent_score == 2 * score:
            score, opponent_score = opponent_score, score
    return score, opponent_score  # You may wish to change this line. 

    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    score, opponent_score = 0, 0
    while score < goal and opponent_score < goal:
        if who == 0:
            score += take_turn(strategy0(score,opponent_score),opponent_score,dice=select_dice(score,opponent_score))
        else:
            opponent_score += take_turn(strategy1(opponent_score,score),score,dice=select_dice(score,opponent_score))
        who = other(who)
        if score != 0 and opponent_score != 0 and (score / opponent_score == 2 or score / opponent_score == 0.5):
                temp = score
                score = opponent_score
                opponent_score = temp
    return score, opponent_score


#######################
# Phase 2: Strategies #
#######################

# Basic Strategy


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    def newf(*args):
        newvar = num_samples
        division = newvar
        count  = 0
        totalvar = 0
        while newvar > 0:
            totalvar = totalvar + fn(*args)
            count+=1
            newvar-=1
        return totalvar/ division
    return newf



def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Print all averages as in
    the doctest below.  Assume that dice always returns positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    1 dice scores 3.0 on average
    2 dice scores 6.0 on average
    3 dice scores 9.0 on average
    4 dice scores 12.0 on average
    5 dice scores 15.0 on average
    6 dice scores 18.0 on average
    7 dice scores 21.0 on average
    8 dice scores 24.0 on average
    9 dice scores 27.0 on average
    10 dice scores 30.0 on average
    10
    """
    save_it = 0
    k=-1
    maximum = 0
    for i in range (1, 11):
        argum = make_averaged(roll_dice, i)
        save_it = argum(i, dice)
        if save_it  > maximum:
            maximum = save_it
            k = i
    return k

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if True: # Change to True to test always_roll(5)
        print('always_roll(8) win rate:', average_win_rate(always_roll(5)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if True: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))
 
    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    digits = [int(number) for number in str(opponent_score)]
    if max(digits) + 1 >= margin:
        return 0
    else:
        return num_rolls

def swap_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls NUM_ROLLS if it would result in a harmfuex swap. It also rolls
    0 dice if that gives at least MARGIN points and rolls
    NUM_ROLLS otherwise.
    """
    digits = [int(number) for number in str(opponent_score)]
    if max(digits) + 1 + score == opponent_score/2:
        return 0
    elif max(digits) + 1 + score == opponent_score * 2: 
        return num_rolls
    else:
        return bacon_strategy(score, opponent_score)


def comeback_strategy(margin, num_rolls=5):
    """Return a strategy that rolls one extra time when losing by MARGIN."""
    "*** YOUR CODE HERE ***"
    def function(score, opponent_score):
        n = num_rolls
        if ( opponent_score - score ) >= margin:           
            n = num_rolls + 1
        return n
    return function

def intent_opponent_fourdie(min_points, num_rolls=5):
    """checks whether or not it is possible to make opponent roll four sided die"""
    def function(score, opponent_score):
        free_bacon = opponent_score // 10 + 1
        if (min_points <= free_bacon) and (((score + free_bacon + opponent_score)%10 == 7) or ((score + free_bacon + opponent_score)%7 == 0)):
            return 0
        else:
            return num_rolls
    return function


def final_strategy(score, opponent_score):
    """Final strategy

    *** YOUR DESCRIPTION HERE ***
    Uses intent_opponent_fourdie strategy and comeback strategy, checks to see if we can win in one turn by using
    free bacon rule, takes less risks when in the lead. 
    
    """
    digits = [int(number) for number in str(opponent_score)] # intent to make opponent roll four die
    free_bacon = max(digits) + 1
    if (score + free_bacon + opponent_score)%7 == 0:
        return 0

    n = 5
    score_loop, opponent_score_loop = 90, 90

    while score_loop != 100: #this will check for one turn win by taking advantage of the free bacon rule
        if opponent_score >= opponent_score_loop and score >= score_loop:
            return 0
        score_loop += 1
        opponent_score_loop -= 10

    if score == opponent_score // 2 - 1:
        return 10

    if score < opponent_score // 2:
        n=4
   

    if (score + opponent_score) % 7 == 0:
        return 3

    if (score - opponent_score) >= 14: #win margin
        n = 4
    if (score - opponent_score) >= 35: #win margin
        n = 3 
    if (opponent_score - score) >= 20: #lose margin
        n = 7
    if (opponent_score - score) >= 40: #lose margin
        n = 8
    n = comeback_strategy(7, n)(score, opponent_score) #lose margin
    n = intent_opponent_fourdie(7,n)(score, opponent_score) 
    return n

def final_strategy_test():
    """Compares final strategy to the baseline strategy."""
    print('-- Testing final_strategy --')
    print('Win rate:', compare_strategies(final_strategy))

def leave_opponent_dice4(score, opponent_score, margin=8, dice=six_sided):
    if score + opponent_score + max(opponent_score//10, opponent_score%10) +1:
        return 0
    else:
        return num_rolls



##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()