---
title: Introduction
layout: default
filename: index
---

# Keyboard Snooping from Audio and Accelerometer Data
UCLA ECE 209AS Project, Winter 2020

## Table of Contents
* [Authors](#authors)
* [Abstract](#abstract)
* [References](#references)

## Authors
- An Le
- Caton Zhong
- Eugene Chu

## Abstract
The problem of keyboard acoustic emanations has shown the possibility of figuring out what a user is typing through keystroke sounds. On the other hand, with the popularity of wearable devices like Apple Watch and Samsung Galaxy Watch, more attack vectors might be exploited. In this project, we present and explore a keyboard snooping attack that utilizes keystroke sounds and accelerometer data collected from compromised wearable devices and mobile phones to determine what a user is typing.

## Literature Review
### Keyboard Acoustic Emanations (2004) [1]
#### Objective
- Show it is possible to eavesdrop different types of keyboards and keypads via acoustic emanations

#### Method
- Use microphone to record sound of each key
- Extract touch peak from audio and perform FFT
- Train NN classifier on key-feature pairs to identify keys
- Repeat for other types of keyboards and various distances

#### Results
- 79% accuracy for {a-z, ';', ',', '.', '/'}
- Accuracy not significantly affected up to 15m
- Degraded accuracy when attacking keyboard using NN trained on another keyboard
- Typing style only affects accuracy slightly
- PC more vulnerable than notebook, but less than phone and ATM pads

### Don't Skype & Type! Acoustic Eavesdropping in Voice-Over-IP [5]
#### Objective
- Identify random keystrokes over Skype, given typing style and keyboard model

#### Method
- Consider different attack scenarios
    - Complete profiling
    - User profiling
    - Model profiling
- Record Skype output
- Perform data segmentation to isolate key sounds
- Use MFCC to extract audio features
- Use k-NN classifier to infer target device
- Use LR classifier to identify keystrokes
- Collect data from users
    - Hunt and Peck, Touch typing styles

#### Results
- 91.7% top-5 accuracy
- \> 90% accuracy when sample length > 20ms
- Better accuracy on higher-quality models such as MacBook Pro
- In model profiling scenario, 60% keystroke accuracy after 10 guesses
    - Still better than random guessing
- Good performance with voice to keystroke ratio < 0dB
- 10<sup>7</sup> fewer tries needed to crack 10-letter password than brute force

## References
[1] D. Asonov and R. Agrawal, “Keyboard acoustic emanations,” in IEEE Symposium  on  Security  and  Privacy,  2004.  Proceedings. 2004.    IEEE, 2004, pp. 3–11.

[2] L.  Zhuang,  F.  Zhou,  and  J.  D.  Tygar,  “Keyboard  acoustic emanations  revisited,” ACM  Transactions  on  Information  and System Security (TISSEC), vol. 13, no. 1, pp. 1–26, 2009.

[3] P.  Marquardt,  A.  Verma,  H.  Carter,  and  P.  Traynor,  “(sp)iphone:  Decoding  vibrations  from  nearby  keyboards  using mobile phone accelerometers,” in Proceedings of the 18th ACM conference  on  Computer  and  communications  security,  2011, pp. 551–562.

[4] J.  Liu,  Y.  Wang,  G.  Kar,  Y.  Chen,  J.  Yang,  and  M.  Gruteser, “Snooping  keystrokes  with  mm-level  audio  ranging  on  a  single  phone,”  in Proceedings  of  the  21st  Annual  International Conference  on  Mobile  Computing  and  Networking,  2015,  pp.142–154.

[5] A.  Compagno,  M.  Conti,  D.  Lain,  and  G.  Tsudik,  “Don’t skype  &  type!  acoustic  eavesdropping  in  voice-over-ip,”  inProceedings of the 2017 ACM on Asia Conference on Computerand Communications Security, 2017, pp. 703–715.

[6] K.  Jin,  S.  Fang,  C.  Peng,  Z.  Teng,  X.  Mao,  L.  Zhang,  and X.  Li,  “Vivisnoop:  Someone  is  snooping  your  typing  without seeing it!” in 2017 IEEE Conference on Communications and Network Security (CNS).    IEEE, 2017, pp. 1–9.

[7] T.  Giallanza,  T.  Siems,  E.  Smith,  E.  Gabrielsen,  I.  Johnson, M. A. Thornton, and E. C. Larson, “Keyboard snooping from mobile  phone  arrays  with  mixed  convolutional  and  recurrent neural  networks,” Proceedings  of  the  ACM  on  Interactive, Mobile, Wearable and Ubiquitous Technologies, vol. 3, no. 2, pp. 1–22, 2019.
