2.

The **NoMemory** Agent is defined as follows:

 if dirt == 1 and wall == 0 and home == 1:

 return vacuum\_cleaning\_agent.SUCK

 if dirt == 1 and wall == 1 and home == 0:

 return vacuum\_cleaning\_agent.SUCK

 if dirt == 1 and wall == 1 and home == 1:

 return vacuum\_cleaning\_agent.SUCK

 if dirt == 1 and wall == 0 and home == 0:

 return vacuum\_cleaning\_agent.SUCK

 if dirt == 0 and wall == 0 and home == 1:

 return vacuum\_cleaning\_agent.FORWARD

 if dirt == 0 and wall == 1 and home == 0:

 return vacuum\_cleaning\_agent.RIGHT

 if dirt == 0 and wall == 1 and home == 1:

 return vacuum\_cleaning\_agent.OFF

 if dirt == 0 and wall == 0 and home == 0:

 return vacuum\_cleaning\_agent.FORWARD

The **Random Agent **is defined as follows:

 action =
list(numpy.random.multinomial(1,self.multinomials1\[(wall,dirt,home)\])).index(1)
+ 1

 return action

 where

 self.multinomials = dict(\[((0,1,1), \[0.1,0,0,0.9,0\]),

 ((1,1,0), \[0,0.1,0.1,0.8,0.0\]),

 ((1,1,1), \[0,0.1,0.1,0.8,0.0\]),

 ((0,1,0), \[0.1,0.1,0.1,0.7,0.0\]),

 ((0,0,1), \[0.6,0.2,0.2,0,0.0\]),

 ((1,0,0), \[0,0.5,0.5,0,0.0\]),

 ((1,0,1), \[0,0.05,0.05,0,0.9\]),

 ((0,0,0), \[0.4,0.3,0.3,0,0.0\]),

 \])

 self.multinomials1 = dict(\[((1,0,1), \[0.0,0.0,0.0,0,1.0\]),

 ((1,1,0), \[0,0.0,0.0,1.0,0\]),

 ((1,1,1), \[0,0.0,0.0,1.0,0.0\]),

 ((1,0,0), \[0.0,0.67,0.33,0.0,0.0\]),

 ((0,0,1), \[0.7,0.15,0.15,0,0.0\]),

 ((0,1,0), \[0,0.0,0.0,1,0.0\]),

 ((0,1,1), \[0,0.0,0.0,1,0.0\]),

 ((0,0,0), \[0.70,0.15,0.15,0,0.0\]),

 \])

The **MemoryModel **is defined as follows:

if self.state == 0 and dirt == 1:

return vacuum\_cleaning\_agent.SUCK

if self.state == 0 and wall == 0:

return vacuum\_cleaning\_agent.FORWARD

if self.state == 0 and wall == 1:

self.state = 1

return vacuum\_cleaning\_agent.RIGHT

if self.state == 1 and wall == 1:

self.state = 6

return vacuum\_cleaning\_agent.RIGHT

if self.state == 1 and wall == 0:

self.state = 2

return vacuum\_cleaning\_agent.FORWARD

if self.state == 2:

self.state = 3

return vacuum\_cleaning\_agent.RIGHT

if self.state == 3 and dirt == 1:

return vacuum\_cleaning\_agent.SUCK

if self.state == 3 and wall == 0:

return vacuum\_cleaning\_agent.FORWARD

if self.state == 3 and wall == 1:

self.state = 4

return vacuum\_cleaning\_agent.LEFT

if self.state == 4 and wall == 1:

self.state = 6

return vacuum\_cleaning\_agent.RIGHT

if self.state == 4 and wall == 0:

self.state = 5

return vacuum\_cleaning\_agent.FORWARD

if self.state == 5:

self.state = 0

return vacuum\_cleaning\_agent.LEFT

if self.state == 6 and home == 1:

return vacuum\_cleaning\_agent.OFF

if self.state == 6 and wall == 0:

return vacuum\_cleaning\_agent.FORWARD

if self.state == 6 and wall == 1:

return vacuum\_cleaning\_agent.RIGHT

**3.**

The best performance recorded by simple reflex agent in the two
environments is as follows:

Map 1=0.503218

Map 2=0.468709

As the simple reflex agent doesn’t have any state to store it’s location
or the percept sequence, it minimizes the agent’s mobility and it can
only crawl through the walls. The number of cells cleaned by the agent
would be equal to the number of corners of the map and therefore, it’s
performance will be adversely affected.

**4.**

The random agent on average performs better than simple reflex
agent,especially in Map 1.

Map 1=0.484146\[over 50 trials\]

Map 2=0.383939\[over 50 trials\]

The random agent performs better when there are no obstructions on
average as it would be difficult for it to come back to the initial
position and hence keeps on moving even after cleaning majority of the
cells.

Fine-tuning the parameters, such as stop etc which can improve
performance \[as the agent stops after more or less squares are empty or
else the no. of moves keep on increasing if it doesn’t stop and
performance deprecates\], probability of stop can be increased to
increase performance and also the turning rate can be increased to
improve performance as the straight line is similar to the simple reflex
agent.

MAP1

  ----- -------------
  Run   Performance
  1     535
  2     533
  3     527
  4     521
  5     518
  6     516
  7     512
  8     511
  9     500
  10    498
  11    498
  12    498
  13    496
  14    490
  15    484
  16    482
  17    480
  18    480
  19    477
  20    477
  21    472
  22    471
  23    470
  24    470
  25    458
  26    445
  27    431
  28    417
  29    415
  30    412
  31    405
  32    396
  33    382
  34    381
  35    375
  36    359
  37    335
  38    312
  39    312
  40    312
  41    312
  42    312
  43    312
  44    311
  45    310
  46    584
  47    585
  48    596
  49    612
  50    858
  ----- -------------

MAP2

  ----- -------------
  RUN   PERFORMANCE
  1     539
  2     554
  3     557
  4     564
  5     582
  6     600
  7     611
  8     612
  9     631
  10    632
  11    632
  12    632
  13    648
  14    658
  15    662
  16    663
  17    664
  18    668
  19    668
  20    669
  21    669
  22    712
  23    741
  24    744
  25    747
  26    748
  27    749
  28    752
  29    755
  30    758
  31    812
  32    814
  33    816
  34    818
  35    820
  36    822
  37    824
  38    826
  39    832
  40    836
  41    844
  42    852
  43    864
  44    872
  45    880
  46    992
  47    1010
  48    1112
  49    1152
  50    1885
  ----- -------------

The average of these 45 best trials in both the cases is

Map1=436

Map2=724

Costs of randomization is that it would take longer to reach the home
position back and to stop, the number of actions may increase.

The advantage of using randomization is that the direction can be
changed and the walls or such obstructions are not such a hindrance to
the performance of the program.

5\. The memory based “Memory Model” which is deterministic performance in
both the maps is as follows:

MAP1=0.472188

MAP2=0.454560

Yes, it is able to clean the room perfectly in both the cases, but the
tradeoff is the number of steps taken by that because it’s memory is
limited. It took 195 steps in the 1^st^ case and 44 steps per room + 20
to change b/w rooms=196 steps in the 2^nd^ case.

Yes, the agent can be improved with more memory to avoid the steps taken
once to repeat, i.e. duplication of traversal can be avoided and the
other advantage would be if it is able to store it’s location in which
case, the agent’s performance can be significantly improved.

6.The trade offs b/w random and deterministic agents are the following:

a\. Deterministic agents have to store a lot of memory which is not
necessary in case of randomized agents.

b\. Randomized agents do not perform well always, they only perform
better on average than simple reflex agents.

c\. Randomness can be useful in cases where there are not many
obstructions or else the no. of steps taken casually \[without achieving
desired result\] are more and hence the performance deprecates.

d\. Deterministic agents are good in areas where there are lots of
obstructions because storing state can be useful to avoid pitfalls in
such cases.

If there are polygonal obstacles, I would try to implement a mix of
random and deterministic memory models where the randomness can help us
deviate away from the object and the model stores such memory to repeat
that path and hence steer away from the polygonal obstacle.

7\. We learn that the simple reflex agents can perform well than random
agents when there are lots of obstructions because they crawl along the
walls, also that the random agents perform better than the simple reflex
agents in case of a simple straight paths. Deterministic memory models
are useful in cases when the storing of state can help us crawl away
from obstacles in the case where a lot of obstacles are present and also
in cases where there is a path without obstructions and maximizing the
throughput irrespective of number of actions is required.

I was surprised to see that the random agent performs bad in comparison
to the simple reflex agent when there are lot of obstructions in the
path because I expected random agent to steer away from obstructions
better than the simple reflex agent. Also, I did not think that the
deterministic memory model would perform similarly well in map 2 with
obstructions in comparison to map 1.
