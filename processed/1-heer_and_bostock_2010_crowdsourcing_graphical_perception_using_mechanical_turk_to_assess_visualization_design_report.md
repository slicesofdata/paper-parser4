# heer-and-bostock-2010-crowdsourcing-graphical-perception--using-mechanical-turk-to-assess-visualization-design

*Auto-assembled report. Section content is drawn from the summarization pipeline outputs.*

## Table of Contents

- [Paper Synthesis](#paper-synthesis)
- [Abstract](#abstract)
- [Introduction (Paper-Level)](#introduction-paper-level)
- [Experiment 1a — Introduction](#experiment-1a-introduction)
- [Experiment 1a — Methods](#experiment-1a-methods)
- [Experiment 1a — Results and Discussion](#experiment-1a-results-and-discussion)
- [Experiment 1b — Introduction](#experiment-1b-introduction)
- [Experiment 1b — Methods](#experiment-1b-methods)
- [Experiment 1b — Results and Discussion](#experiment-1b-results-and-discussion)
- [Experiment 2 — Introduction](#experiment-2-introduction)
- [Experiment 2 — Methods](#experiment-2-methods)
- [Experiment 2 — Results and Discussion](#experiment-2-results-and-discussion)
- [Experiment 3 — Introduction](#experiment-3-introduction)
- [Experiment 3 — Methods](#experiment-3-methods)
- [Experiment 3 — Results and Discussion](#experiment-3-results-and-discussion)
- [General Discussion](#general-discussion) *(not available)*
- [Critique](#critique)

<a name="paper-synthesis"></a>
## Paper Synthesis

*Paper: heer-and-bostock-2010-crowdsourcing-graphical-perception--using-mechanical-turk-to-assess-visualization-design*

### Executive Summary

The paper investigates whether Amazon Mechanical Turk can serve as a viable platform for graphical perception experiments, replicating classic Cleveland & McGill findings and extending them to new tasks such as rectangular area judgments, luminance contrast, and chart size/gridline spacing. It finds that crowdsourced participants generally reproduce the established ranking of visual encodings (position > length > area > angle) and that rectangular area judgments match circular ones, while also revealing specific divergences (angle not worse than length, and square aspect ratios yielding the poorest performance). The study concludes that MTurk provides low‑cost, scalable, and largely valid perception measurements for a range of visual variables.

### Reading Recommendation

**Read Selectively**

The paper offers novel crowdsourced replications of classic graphical perception findings and new insights on rectangular area judgments, chart size, and gridline spacing, which merit detailed reading of the methods and results sections. However, high‑severity methodological and statistical shortcomings (missing interaction tests, lack of power analysis, and contradictory evidence for angle vs. length) and overgeneralized claims reduce its overall impact, so a full read is not essential.

### Background and Motivation

The paper addresses the gap that it is unknown whether crowdsourced graphical‑perception experiments, which lack control over display hardware, lighting, and viewing distance, can reliably reproduce classic laboratory findings and thus provide valid design guidance for visualizations. This question is motivated by the foundational work of Cleveland & McGill on perceptual effectiveness of visual encodings, Bertin’s systematic taxonomy of visual variables, and more recent surveys of web‑based experimentation by Kohavi et al. and the demonstration of MTurk’s potential for reliable data collection by Kittur et al. (and later by Mason & Watts on compensation effects).

### Theoretical Stance

**Overall stance: Consistent Theoretical**

The introduction foregrounds graphical‑perception theory and a crowdsourcing‑viability stance, and the discussion repeatedly interprets the replication and new results through those same frameworks, maintaining alignment across sections despite some contradictory findings.

#### Theories Discussed

- **Graphical perception theory (Cleveland & McGill)** *(focal)*: Defines graphical perception as the ability to interpret visual encodings; provides psychophysical rankings of visual variables (e.g., position > length > area > angle).
- **Crowdsourcing viability theory** *(focal)*: Posits that Amazon Mechanical Turk can serve as a low‑cost, scalable platform for conducting reliable graphical‑perception experiments despite limited environmental control.
- **Laboratory‑based perception theory** *(alternative)*: Claims that strict control over display, lighting, and viewing conditions is necessary for valid perception measurements, contrasting with the crowdsourcing approach.
- **Bertin’s visual‑variable taxonomy** *(background)*: Systematic classification of visual variables (position, length, area, color, etc.) that underlies the ranking of encoding effectiveness.
- **Psychophysical theory of visual‑encoding rankings** *(background)*: Specific predictions that area performs worse than angle, and angle performs worse than length, derived from classic psychophysical work.
- **Crowdsourcing scalability account** *(background)*: General claim that web‑based crowdsourcing enables large‑scale, diverse subject recruitment, improving ecological validity of perception studies.


### Study Design

- **Number of experiments:** 4
- **Predictors examined:** judgment type (T1–T7), display (T8 vs. T9), aspect ratio (various rectangular ratios), background (5 levels), density (4 levels), chart type (bar vs. line), chart height (40, 80, 160 pixels), gridline spacing (10, 20, 50, 100 units)
- **Outcomes examined:** estimated percentage (free‑text proportion estimate), percentage estimate for rectangular area judgments, alpha value (gridline contrast adjustment), estimation error (absolute difference between judged and true values), response time / time to completion (recorded via JavaScript or timing logs)
- **Materials:** Stimuli were computer‑generated charts and shapes rendered at fixed pixel resolutions (e.g., 380×380 px for Cleveland & McGill replication, 600×400 px treemap displays, 450×300 px gridline charts). Visual encodings included position, length, angle, area (circular and rectangular), luminance contrast grids, and bar/line charts with varying heights and gridline spacings.
- **Design types:**
  - exp_1A: within‑subjects 7‑level judgment‑type (T1–T7) design
  - exp_1B: within‑subjects 2 (display) × 9 (aspect‑ratio) factorial design
  - exp_2: within‑subjects 5 (background) × 4 (density) factorial design
  - exp_3: within‑subjects 2 (chart type) × 3 (height) × 4 (gridline spacing) factorial design

### Findings Summary

Across the four experiments, crowdsourced participants on Mechanical Turk reproduced the classic ranking of visual encodings—position outperformed length, which outperformed area and angle—though the expected superiority of length over angle was not observed. Rectangular area judgments were as accurate as circular area judgments, yet aspect ratio had a surprising main effect: perfectly square rectangles yielded the poorest performance, contrary to the hypothesis that extreme (non‑square) ratios would be detrimental. In the luminance‑contrast study, plot density influenced participants' chosen alpha values, while background intensity did not, and several display‑related factors (screen resolution, color depth, operating system) showed modest correlations with contrast settings. Finally, chart height and gridline spacing both significantly affected estimation error, with very short (40 px) charts producing higher errors and an interaction indicating that dense gridlines exacerbate errors at low heights; increasing chart height beyond 80 px and spacing gridlines at least 8 px apart offered no further accuracy gains. Together, these results demonstrate that MTurk can yield valid perception measurements for a range of visual variables, while also revealing specific divergences from theoretical predictions in angle versus length performance and aspect‑ratio effects.

### Evidence–Claim Alignment

#### Supported Claims

- Crowdsourced experiments can replicate the classic ranking of visual encodings (position > length > area > angle), as shown by the preserved ranking of judgment types in Experiment 1A.
- Rectangular area judgments are as accurate as circular area judgments, supported by the main effect in Experiment 1B showing matching accuracy across display types.
- Higher compensation speeds data collection without substantially degrading overall response quality, evidenced by Experiment 3 where increased pay reduced elapsed time to HIT completion while only a small accuracy drop was observed.
- Qualification tasks and verifiable questions improve data quality, reflected in low outlier rates (0.75%) and high overall response quality reported across experiments.


#### Unsupported or Weakly Supported Claims

- Angle encoding should perform worse than length encoding; Experiment 1A found no performance difference, contradicting the theoretical prediction.
- Extreme aspect ratios should impair rectangular area judgments; Experiment 1B found the worst performance at aspect ratio = 1 (square), opposite to the hypothesis.
- Crowdsourced results are comparable to laboratory results for luminance contrast tasks; Experiment 2 shows significant effects of display‑related variables (screen resolution, color depth, OS) that are not present in the original lab study, leaving the claim only weakly supported.


#### Contradictions or Tensions

- The paper concludes that crowdsourced perception experiments are broadly viable for visualization design, yet the evidence is limited to a subset of encodings (position, length, area, angle, contrast, chart size, gridline spacing) and does not address many other visual variables, creating a tension between the broad claim and the narrow empirical scope.
- The introduction asserts that higher pay influences speed but not accuracy, while Experiment 3 reports a statistically significant reduction in accuracy under higher pay, directly contradicting the mechanistic claim.
- The authors claim that loss of environmental control limits experiment scope but still generalize the viability of crowdsourcing to all visualization design tasks, which conflicts with their own acknowledgment of this limitation.


### Strengths

- Methodological rigor: multiple within‑subjects factorial experiments (replication of classic studies, new area, contrast, and chart‑size tasks) with large sample sizes (e.g., 3500 judgments in Exp 1A).
- Transparent reporting of cost and time: detailed compensation levels, HIT counts, and speed gains from higher pay are provided.
- Successful replication of classic Cleveland & McGill rankings for most encodings (position > length > area > angle) using crowdsourced participants.
- Novel contributions: first crowdsourced investigations of rectangular area judgments, aspect‑ratio effects, luminance‑contrast settings, and chart‑height/gridline‑spacing interactions.
- Effective quality controls: qualification tasks and verifiable questions yielded low outlier rates (0.75 %) and high overall response quality.
- Converging evidence across four experiments supports the viability of MTurk for a range of visual‑encoding measurements.


### Weaknesses and Concerns

- Theoretical misalignment: angle encoding did not perform worse than length, directly contradicting a core psychophysical prediction yet the authors downplay this inconsistency while claiming overall validity.
- Aspect‑ratio hypothesis failure: the worst performance occurred at aspect ratio = 1, opposite to the predicted detrimental effect of extreme ratios, and the paper offers no reconciliation.
- Overgeneralization: the conclusion that crowdsourced perception experiments are broadly viable for visualization design extends beyond the limited set of encodings tested and ignores the acknowledged loss of control over display conditions.
- Internal inconsistency on compensation: the introduction asserts higher pay affects speed only, but Experiment 3 reports a statistically significant reduction in accuracy under higher pay.
- Statistical reporting gaps: several factorial designs omit key interaction tests (e.g., missing interaction in Exp 1B, Exp 2, and especially multiple main effects and interactions in Exp 3), and effect sizes or confidence intervals are absent for most reported p‑values.
- Methodological omissions: no a priori power analyses, no demographic or exclusion reporting, and no preregistration, limiting reproducibility and assessment of sample representativeness.
- Multiple‑comparison risk: numerous ANOVAs and post‑hoc tests are presented without correction for family‑wise error, raising the possibility of inflated Type I error rates.


### Key References

- **Cleveland & McGill (1970s)** — foundational theory
- **Bertin (2)** — foundational theory
- **Kohavi et al. (15)** — primary methodological precedent
- **Mason & Watts (23)** — key empirical precedent
- **Kittur et al. (14)** — primary methodological precedent
- **Stone & Bartram (30)** — key empirical precedent
- **Bruls et al. (2000)** — primary methodological precedent
- **Cole et al. (8)** — primary methodological precedent
- **Heer & Bostock (21)** — theoretical prediction source
- **Heer & Bostock (13)** — key empirical precedent

<a name="abstract"></a>
## Abstract

*Preserved from source without summarization.*

Understanding perception is critical to effective visualization design. With its low cost and scalability, crowdsourcing presents an attractive option for evaluating the large design space of visualizations; however, it first requires validation. In this paper, we assess the viability of Amazon’s Mechanical Turk as a platform for graphical perception experiments. We replicate previous studies of spatial encoding and luminance contrast and compare our results. We also conduct new experiments on rectangular area perception (as in treemaps or cartograms) and on chart size and gridline spacing. Our results demonstrate that crowdsourced perception experiments are viable and contribute new insights for visualization design. Lastly, we report cost and performance data from our experiments and distill recommendations for the design of crowdsourced studies.

ACM Classification: H5.2 [Information interfaces and presentation]: User Interfaces—Evaluation/Methodology

General Terms: Experimentation, Human Factors.

Keywords: Information visualization, graphical perception, user study, evaluation, Mechanical Turk, crowdsourcing.

<a name="introduction-paper-level"></a>
## Introduction (Paper-Level)

*Section: paper-level*

### Research Gap / Motivation

It remains unclear whether crowdsourced perception experiments, which lack control over display and environmental factors, can reliably replicate laboratory findings and provide valid insights for visualization design.


### Theoretical Framework

- **crowdsourcing viability for graphical perception**
  > In this work, we investigate if crowdsourced experiments insensitive to environmental context are an adequate tool for graphical perception research.

- **graphical perception theory**
  > Following Cleveland [7], we use the term graphical perception to denote the ability of viewers to interpret such visual encodings and thereby decode information in graphs.
  - Citations: Cleveland (7)

### Specific Hypotheses / Predictions

- **replication of laboratory results**
  > We replicate prior laboratory studies on spatial data encodings and luminance contrast using crowdsourcing techniques. Our new results match previous work, are consistent with theoretical predictions [21].
  - Citations: Heer & Bostock (21)
- **new insights from crowdsourced experiments**
  > We demonstrate the use of crowdsourcing to generate new perception results. We conduct experiments investigating area judgments, chart size and gridline spacing.

- **effect of qualification tasks on response quality**
  > We find that qualification tasks and verifiable questions help ensure high-quality responses.

- **compensation level influences speed not accuracy**
  > experimenters can accelerate the time to results by increasing the compensation level.


### Mechanistic Claims

- **qualification tasks improve data quality**
  > qualification tasks and verifiable questions help ensure high-quality responses

- **higher pay speeds data collection**
  > experimenters can accelerate the time to results by increasing the compensation level

- **environmental context loss limits experiment scope**
  > Crowdsourced perception experiments lack control over many experimental conditions, including display type and size, lighting, and subjects’ viewing distance and angle. This loss of control inevitably limits the scope of experiments that reliably can be run.


### Constructs of Interest

- **crowdsourced experimental platform (MTurk)** *(predictor)*: use of Amazon Mechanical Turk to recruit participants and present visual perception tasks.
- **graphical perception performance** *(outcome)*: accuracy and response time of participants when estimating values from visual encodings.


### Rationale for Predictor

Crowdsourcing offers a low‑cost, scalable way to recruit large, diverse subject pools and to run many visual perception tasks quickly, potentially increasing ecological validity.


### Rationale for Outcome

Assessing graphical perception performance is essential for validating visual encoding effectiveness and guiding visualization design.


### Key Terminology

- **graphical perception:** the ability of viewers to interpret visual encodings and decode information in graphs
  > Following Cleveland [7], we use the term graphical perception to denote the ability of viewers to interpret such visual encodings and thereby decode information in graphs.
- **crowdsourcing:** a phenomenon where web workers complete small tasks for micro‑payments, providing a scalable, low‑cost means of conducting user studies
  > “Crowdsourcing” is a relatively new phenomenon in which web workers complete one or more small tasks, often for micro‑payments on the order of \0.01 to \0.10 per task.


### Background Research

- Cleveland & McGill (7) demonstrated that visual variables differ in perceptual effectiveness for quantitative encoding.
- Bertin (2) provided a systematic treatment of visual variables that inspired rankings of position, length, area, and color.
- Kohavi et al. (15) surveyed web experiment design and highlighted its growing acceptance.
- Mason & Watts (23) showed that higher compensation increases response quantity but not accuracy.


### Alternative Theories Discussed

#### laboratory‑based perception theory

- **Description:** Traditional view that controlled laboratory settings are necessary to obtain reliable graphical perception measurements because they eliminate environmental variability.
- **Difference from focal theory:** Emphasizes strict control over display, lighting, and viewing conditions, predicting that results obtained without such control (e.g., crowdsourced) may be unreliable.
- **Citations:** Cleveland & McGill (7)

### Overview of Studies

The paper describes three sets of experiments: (1) replication of Cleveland & McGill’s spatial encoding study and Stone & Bartram’s contrast study; (2) new experiments on area judgments, chart height, and gridline spacing; (3) analysis of MTurk performance and cost across all experiments.


### Missing or Unclear

- explicit statement of a formal theoretical model linking crowdsourcing characteristics to perception accuracy
- detailed mediating variables explaining how environmental variability impacts perception outcomes
- pre-registered hypotheses or statistical power analyses


### All Citations Referenced

- **Cleveland (7)** — graphical perception definition and classic study
- **Bertin (2)** — systematic treatment of visual variables
- **Kohavi et al. (15)** — web experiment design survey
- **Mason & Watts (23)** — compensation effects on quantity vs. quality
- **Heer & Bostock (21)** — theoretical predictions for visual encodings
- **Stone & Bartram (30)** — alpha contrast experiment
- **Kittur et al. (14)** — MTurk quality judgments
- **Cole et al. (8)** — MTurk perception experiment
- **Cleveland & McGill (7)** — classic proportionality study
- **Heer & Bostock (13)** — ecological validity concerns
- **Heer & Bostock (14)** — subject motivation and expertise
- **Heer & Bostock (23)** — subject motivation and expertise
- **Heer & Bostock (27)** — visual variable rankings
- **Heer & Bostock (34)** — visual variable interactions
- **Heer & Bostock (10)** — visual variable interactions
- **Heer & Bostock (12)** — chart size effects
- **Heer & Bostock (6)** — scale effects
- **Heer & Bostock (1)** — aspect ratio effects
- **Heer & Bostock (5)** — aspect ratio effects
- **Heer & Bostock (33)** — visualizations online
- **Heer & Bostock (35)** — visualizations online


### Additional Quoted Evidence

> In this work, we investigate if crowdsourced experiments insensitive to environmental context are an adequate tool for graphical perception research.

> We replicate prior laboratory studies on spatial data encodings and luminance contrast using crowdsourcing techniques. Our new results match previous work, are consistent with theoretical predictions [21].

> Crowdsourced perception experiments lack control over many experimental conditions, including display type and size, lighting, and subjects’ viewing distance and angle.

<a name="experiment-1a-introduction"></a>
## Experiment 1a — Introduction

*Section: exp_1a*

### Rationale for This Experiment

The experiment is run to replicate Cleveland & McGill’s seminal study on Mechanical Turk in order to assess the viability of crowdsourcing for graphical perception research.


### Relation to Prior Experiments

This is the first experiment in the paper, establishing a baseline replication before subsequent experiments build on it.







### Missing or Unclear

- No specific predictions are stated for this experiment.
- No theoretical refinements or new alternative theories are introduced.
- No new manipulation, sample source, or procedural detail is described.


### Citations Referenced

- **Cleveland & McGill (1970s)** — seminal study on visual variables effectiveness
- **Authors of references 21 and 22 (unknown)** — automated presentation techniques
- **Authors of reference 36 (unknown)** — extensions of Cleveland & McGill’s work

<a name="experiment-1a-methods"></a>
## Experiment 1a — Methods

*Section: exp_1a*

### Participants

- **N:** 3500
- **Recruitment:** Mechanical Turk
- **Compensation:** 0.05 per judgment
- **Testing context:** online via Mechanical Turk

### Design

**Design statement:** 7 (judgment type: T1–T7) within-subjects design.

**Predictors:**

- **judgment type**
  - Levels: T1, T2, T3, T4, T5, T6, T7
  - Manipulation: within-subjects
  - Factor type: nominal

**Counterbalancing:** not reported

### Outcome Measures

- **estimated percentage:** free‑text estimate of the smaller value as a percentage of the larger value

### Materials

- **Description:** Charts representing visual encodings (position, length, angle, area) constructed at 380×380 pixels.
- **Source:** mimicked original Cleveland & McGill charts
- **Stimulus pool size:** 10
- **Stimuli presented per participant:** 10 per participant (one of each type)
- **Additional details:**
  - resolution 380×380 pixels
  - seven judgment types correspond to visual encodings

### Procedure

**Ordered steps:**

1. Complete qualification test with two example charts and three test charts
2. For each chart task, identify the smaller of two marked values
3. Make a quick visual judgment to estimate the percentage the smaller value is of the larger

- **Apparatus:** Mechanical Turk platform, web browser
- **Experimenter presence:** remote (online)
- **Presentation format:** each chart presented as an individual HIT; sequence not counterbalanced
- **Stimulus timing:** not reported

**Verbatim instructions (as quoted in the paper):**

> identify the smaller of two marked values

> make a quick visual judgment


### Preregistration and Analysis Plan

- **Preregistration:** not reported


### Author-Provided Rationale for Methodological Choices

- Qualification test ensured subjects understood instructions without filtering inaccurate subjects
- Using individual HITs avoided issues with long tasks on Mechanical Turk

### Missing or Unclear

- Demographic details (age, gender, education) not provided
- Power analysis not reported
- Explicit exclusion criteria not stated
- Stimulus timing (duration, ISI) not reported
- Session duration not reported
- Details of randomization or counterbalancing scheme not reported
- Apparatus specifics beyond platform not described
- Pre‑registration status not mentioned
- Data analysis plan not described

### Citations Referenced in This Section

- **Cleveland & McGill ()** — original experiment providing the charts and within‑subjects format

### Quoted Evidence from Source

> Ten charts were constructed at a resolution of 380×380 pixels, for a total of 70 trials (HITs).

> Subjects were paid \0.05 per judgment.

> For each chart, N=50 subjects were instructed first to identify the smaller of two marked values, and then “make a quick visual judgment” to estimate what percentage the smaller was of the larger.

<a name="experiment-1a-results-and-discussion"></a>
## Experiment 1a — Results and Discussion

*Section: exp_1a*

### Statistical Approach

We first computed the midmeans of log absolute errors for each chart (Figure 3). Next we computed the log absolute error means and 95% confidence intervals for each judgment type using bootstrapping (c.f., [7]).


### Key Findings

#### The ranking of judgment types by accuracy is preserved in the crowdsourced study

- **Test:** midmeans of log absolute errors
- **Effect type:** main effect
- **Variables in model:** chart type, judgment type, accuracy

**Verbatim statistical report:**

> The new results are similar (though not identical) to the originals: the rough shape and ranking of judgment types by accuracy (T1-5) are preserved, supporting the validity of the crowdsourced study.


#### Types 1 and 2 are closer in the crowdsourced study

- **Test:** log absolute error means and 95% confidence intervals
- **Effect type:** main effect
- **Variables in model:** judgment type, accuracy

**Verbatim statistical report:**

> Types 1 and 2 are closer in the crowdsourced study; this may be a result of a smaller display mitigating the effect of distance.


#### Types 4 and 5 are more accurate than in the original study

- **Test:** log absolute error means and 95% confidence intervals
- **Effect type:** main effect
- **Variables in model:** judgment type, accuracy

**Verbatim statistical report:**

> Types 4 and 5 are more accurate than in the original study, but position encoding still significantly outperformed length encoding.


#### Area performs worse than angle, and both are worse than position

- **Test:** log absolute error means and 95% confidence intervals
- **Effect type:** main effect
- **Variables in model:** judgment type, accuracy

**Verbatim statistical report:**

> Indeed, the new results match expectations: psychophysical theory [7,34] predicts area to perform worse than angle, and both to be significantly worse than position.

- Citations: Cleveland & McGill (1984)

#### Angle does not perform worse than length

- **Test:** log absolute error means and 95% confidence intervals
- **Effect type:** main effect
- **Variables in model:** judgment type, accuracy

**Verbatim statistical report:**

> Theory also suggests that angle should perform worse than length, but the results do not support this.



### Authors' Interpretations

- **validity of crowdsourced study**
  > The new results are similar (though not identical) to the originals: the rough shape and ranking of judgment types by accuracy (T1-5) are preserved, supporting the validity of the crowdsourced study.

- **comparison of judgment types**
  > Types 1 and 2 are closer in the crowdsourced study; this may be a result of a smaller display mitigating the effect of distance. Types 4 and 5 are more accurate than in the original study, but position encoding still significantly outperformed length encoding.

- **performance of angle and area encodings**
  > Indeed, the new results match expectations: psychophysical theory [7,34] predicts area to perform worse than angle, and both to be significantly worse than position. Theory also suggests that angle should perform worse than length, but the results do not support this.
  - Citations: Cleveland & McGill (1984)

### Authors' Stated Links to Their Own Predictions

- **performance of angle and area encodings**
  > Indeed, the new results match expectations: psychophysical theory [7,34] predicts area to perform worse than angle, and both to be significantly worse than position.
  - Citations: Cleveland & McGill (1984)
- **performance of angle relative to length**
  > Theory also suggests that angle should perform worse than length, but the results do not support this.


### Anomalous or Unexpected Results (as characterized by authors)

- Theory also suggests that angle should perform worse than length, but the results do not support this.






### Citations Referenced

- **Cleveland & McGill (1984)** — psychophysical theory
- **Cleveland & McGill (1984)** — position-angle experiment
- **Cleveland & McGill (1984)** — position-length experiment

<a name="experiment-1b-introduction"></a>
## Experiment 1b — Introduction

*Section: exp_1b*

### Rationale for This Experiment

To extend the replication beyond circular area judgments by examining rectangular area judgments, assess the impact of aspect ratio variations, and explore whether treemap design algorithms are perceptually optimal.


### Relation to Prior Experiments

Follows Experiment 1A which replicated Cleveland & McGill’s results for circular area judgments; Experiment 1B adds rectangular judgments and new manipulations.


### Specific Predictions

- **performance similar to circular area judgments**
  > We hypothesized that, on average, subjects would perform similarly to the circular case, but that performance would be impacted by varying the aspect ratios of the compared shapes.

- **aspect ratio hampers area judgments**
  > Based on prior results [19,34], we were confident that extreme variations in aspect ratio would hamper area judgments.
  - Citations: 19 (); 34 ()
- **distracting elements may bias estimation**
  > We also wanted to assess if other differences, such as the presence of additional distracting elements, might bias estimation.


### Theoretical Refinements (relative to paper-level intro)

- **rectangular area judgments relevance**
  > We sought to compare our circular area judgment (T7) results with rectangular area judgments arising in visualizations such as cartograms [9] and treemaps [26].
  - Citations: 9 (); 26 ()
- **squarified treemap perceptual optimality question**
  > “Squarified” treemap algorithms [3,35] address this issue by attempting to minimize deviance from a 1:1 aspect ratio, but it is unclear that this approach is perceptually optimal.
  - Citations: 3 (); 35 ()


### New Elements Introduced

- rectangular area judgment task
- manipulation of aspect ratios of compared shapes
- inclusion of distracting visual elements
- comparison to cartograms and treemaps


### Constraints Addressed

- tests boundary condition of aspect ratio effects on area perception
- evaluates perceptual optimality of squarified treemap algorithms
- examines potential bias from distracting elements



### Citations Referenced

- **9 ()** — cartograms
- **26 ()** — treemaps
- **19 ()** — prior results on aspect ratio effects
- **34 ()** — prior results on aspect ratio effects
- **3 ()** — squarified treemap algorithm
- **35 ()** — squarified treemap algorithm

<a name="experiment-1b-methods"></a>
## Experiment 1b — Methods

*Section: exp_1b*

### Participants

- **Compensation:** 0.02 USD per HIT

### Design

**Design statement:** 2 (display: T8 vs. T9) x 9 (aspect ratio levels) within-subjects factorial design.

**Predictors:**

- **display**
  - Levels: T8, T9
  - Manipulation: within-subjects
  - Factor type: nominal
- **aspect ratio**
  - Levels: 2/3, 1, 3/2, 2/3 x 2/3, 2/3 x 1, 2/3 x 3/2, 1 x 2/3, 1 x 1, 1 x 3/2, 3/2 x 2/3, 3/2 x 1, 3/2 x 3/2
  - Manipulation: within-subjects
  - Factor type: nominal

**Counterbalancing:** not reported

### Outcome Measures

- **percentage estimate:** participants estimated the percentage that the smaller rectangle was of the larger rectangle

### Materials

- **Description:** Two rectangles (marked A or B) displayed either with horizontally aligned centers (T8) or as 600×400 pixel treemaps (T9) showing 24 values; aspect ratios varied systematically.
- **Source:** Adapted from Cleveland & McGill proportional judgment task; treemap layout based on Bruls et al.
- **Stimulus pool size:** 108 unique trials (HITs)
- **Additional details:**
  - Aspect ratios derived from cross‑product of {2/3, 1, 3/2} with itself
  - Treemaps generated from 1,000 random treemaps of 24 values

### Procedure

**Ordered steps:**

1. Qualification task using multiple‑choice versions of two trial stimuli (one per display condition)
2. Main experiment: participants completed proportional judgment trials (108 HITs total, 6 replications per condition)
3. Responses recorded via MTurk platform

- **Apparatus:** Amazon Mechanical Turk (online platform)
- **Experimenter presence:** remote
- **Presentation format:** not reported
- **Stimulus timing:** not reported


### Preregistration and Analysis Plan

- **Preregistration:** not reported


### Author-Provided Rationale for Methodological Choices

- Reward per HIT reduced to $0.02 in an attempt to match the U.S. national minimum wage assuming a response time of 10 seconds per trial

### Missing or Unclear

- total number of participants (N) not reported
- demographic information (age, gender, etc.) not reported
- recruitment source not specified
- exclusion criteria not stated
- testing context (individual vs. group, lab vs. online session length) not described
- counterbalancing scheme not described
- stimulus timing details (duration, ISI) not provided
- session duration not reported
- data analysis plan not detailed
- preregistration status not indicated
- power analysis not performed or reported

### Citations Referenced in This Section

- **Cleveland & McGill (1970s)** — original proportional judgment task used as basis for the experiment
- **Bruls et al. (2000)** — layout algorithm used to generate treemaps for stimulus creation

### Quoted Evidence from Source

> We used a 2 (display) × 9 (aspect ratios) factorial design with 6 replications for a total of 108 unique trials (HITs).

> As a qualification task, we used multiple-choice versions of two trial stimuli, one for each display condition.

> We also reduced the reward per HIT to \0.02.

<a name="experiment-1b-results-and-discussion"></a>
## Experiment 1b — Results and Discussion

*Section: exp_1b*

### Statistical Approach

To facilitate comparison across studies, we used Cleveland & McGill’s log absolute error measure. We omitted 16 responses (0.62%), for which the subject’s estimate differed from the true difference by more than 40%.


### Key Findings

#### Accuracy of rectangular area judgments matches that of circular area judgments

- **Test:** ANOVA
- **Effect type:** main effect
- **Variables in model:** display type, true proportions, judgment accuracy

**Verbatim statistical report:**

> The results confirm our hypothesis that, on average, the accuracy of rectangular area judgments matches that of circular area judgments.

**Verbatim descriptives:**

> Midmeans for each display type are included in Figure 3. Confidence intervals are shown in Figure 4.


#### Aspect ratio significantly affects judgment accuracy

- **Test:** ANOVA
- **Effect type:** main effect
- **Variables in model:** aspect ratio, judgment accuracy

**Verbatim statistical report:**

> We found a significant (p < 0.05) effect of aspect ratio on judgment accuracy, as shown in Figure 5.

**Verbatim descriptives:**

> Somewhat surprisingly, comparisons of rectangles with aspect ratio 1 exhibited the worst performance, a result robust across both the rectangle and treemap display conditions.


#### No significant difference between rectangle and treemap conditions

- **Test:** ANOVA
- **Effect type:** main effect
- **Variables in model:** display type, judgment accuracy

**Verbatim statistical report:**

> We found no significant difference between the rectangle (T8) and treemap (T9) conditions, suggesting that other elements in a treemap display do not interfere with judgment accuracy.



### Authors' Interpretations

- **Aspect ratio effect**
  > This finding suggests that viewers actually benefit from the inability of a squarified treemap algorithm to perfectly optimize the rectangles to 1:1 aspect ratios. The result is consistent with the hypothesis that viewers use 1D length comparisons to help estimate area: comparing the lengths of sides as a proxy for area leads to maximal error when comparing squares.

- **Rectangle vs. treemap**
  > We found no significant difference between the rectangle (T8) and treemap (T9) conditions, suggesting that other elements in a treemap display do not interfere with judgment accuracy.


### Authors' Stated Links to Their Own Predictions

- **Accuracy of rectangular vs. circular area judgments**
  > The results confirm our hypothesis that, on average, the accuracy of rectangular area judgments matches that of circular area judgments.


### Anomalous or Unexpected Results (as characterized by authors)

- Somewhat surprisingly, comparisons of rectangles with aspect ratio 1 exhibited the worst performance, a result robust across both the rectangle and treemap display conditions.



### Limitations Stated by Authors

- However, as we lack control over subjects’ display configuration, we must first establish the reliability of crowdsourced studies involving luminance contrast.


### Preview of Next Experiment

We take up this issue in our next experiment.


### Missing or Unclear (Non-Statistical)

- No specific details about the statistical tests used (e.g., ANOVA, t-tests) or the exact sample sizes for each condition.

<a name="experiment-2-introduction"></a>
## Experiment 2 — Introduction

*Section: exp_2*

### Rationale for This Experiment

To extend crowdsourced graphical perception research from spatial encodings to luminance contrast tasks, assess whether crowd data can replicate laboratory findings, and evaluate how uncontrolled display conditions influence results.


### Relation to Prior Experiments

Experiment 2 follows earlier experiments on black‑and‑white spatial encodings and introduces a new perceptual dimension (alpha contrast) to test the generality of crowdsourced methods.


### Specific Predictions

- **crowdsourced results comparable to lab**
  > a successful replication would help establish the utility of crowd-sourced experiments for a broader range of perception tasks.
  - Citations: Stone & Bartram (30)
- **display configuration impacts outcomes**
  > We expect monitor display settings and lighting conditions to affect the outcome of this task.

- **higher variance but similar means**
  > results may exhibit higher variance, but with means suitable for a larger user population.


### Theoretical Refinements (relative to paper-level intro)

- **luminance contrast bounds for reference elements**
  > The experiment seeks to bound the range of acceptable luminance contrast settings for visual reference elements such as gridlines.

- **utility of crowdsourcing for broader perception tasks**
  > a successful replication would help establish the utility of crowd-sourced experiments for a broader range of perception tasks.
  - Citations: Stone & Bartram (30)


### New Elements Introduced

- alpha contrast manipulation of gridline transparency
- varying background darkness levels
- different plot density conditions
- assessment of monitor display settings and ambient lighting


### Constraints Addressed

- effects of monitor display settings and lighting on perception
- generalization of crowdsourced methods to luminance contrast tasks


### Missing or Unclear

- explicit statistical power or sample size details
- specific measurement instruments for display configuration


### Citations Referenced

- **Stone & Bartram (30)** — original alpha contrast experiment

<a name="experiment-2-methods"></a>
## Experiment 2 — Methods

*Section: exp_2*

### Participants

- **N:** 24
- **Recruitment:** MTurk
- **Compensation:** 0.02 per HIT
- **Testing context:** online via Flash embedded frame

### Design

**Design statement:** 5 (background) × 4 (density) within-subjects factorial design with 3 replications, 60 trials per task.

**Predictors:**

- **background**
  - Levels: level 1, level 2, level 3, level 4, level 5
  - Manipulation: within-subjects
  - Factor type: nominal
- **density**
  - Levels: level 1, level 2, level 3, level 4
  - Manipulation: within-subjects
  - Factor type: nominal

**Counterbalancing:** not reported

### Outcome Measures

- **alpha value:** recorded from JavaScript as the contrast adjustment value (0-255 scale)
- **time to completion:** recorded for each trial via JavaScript timing
- **screen resolution:** reported by JavaScript
- **color depth:** reported by JavaScript
- **browser type (User-Agent):** reported by JavaScript

### Materials

- **Description:** chart display with gridlines and alpha adjustment controls (Lighter/Darker buttons)
- **Source:** in-house Flash application with custom JavaScript
- **Stimulus pool size:** 20 (5 backgrounds × 4 densities)
- **Stimuli presented per participant:** 60 trials per participant per task
- **Additional details:**
  - plot size 450×300 pixels
  - frame height 700 pixels
  - background varied to fill majority of a standard laptop display

### Procedure

**Ordered steps:**

1. Qualification task: adjust sample display to fully transparent (alpha=0) or fully opaque (alpha=1)
2. Main task L or D presented via Flash applet embedded in MTurk frame
3. Participant reads task-specific instruction
4. Participant adjusts grid alpha using Lighter/Darker buttons
5. Data (alpha value, timing, screen info) recorded via JavaScript
6. Submit HIT

- **Apparatus:** Flash application embedded in web page, custom JavaScript, MTurk platform
- **Experimenter presence:** absent
- **Presentation format:** randomized trials
- **Stimulus timing:** not reported
- **Session duration:** not reported

**Verbatim instructions (as quoted in the paper):**

> Adjust the grid so that it is as light as possible while still being usably perceptible.

> Adjust the grid strength to meet your best judgment of how obvious it can be before it becomes too intrusive and sits in front of the image; some users have called this a ‘fence’.


### Preregistration and Analysis Plan

- **Preregistration:** not reported


### Author-Provided Rationale for Methodological Choices

- Interactivity required, so standard MTurk markup could not be used; Flash applet hosted to allow custom controls
- Custom JavaScript used to collect display configuration data unavailable in standard MTurk interface

### Missing or Unclear

- Power analysis not reported
- Exclusion criteria not stated
- Demographic details (age, gender, etc.) not provided
- Session duration not specified
- Stimulus timing details not provided
- Counterbalancing scheme not described
- Randomization method not detailed
- Number of participants per condition not given

### Citations Referenced in This Section

- **Stone & Bartram (30)** — lab study shown in Figure 8 for comparison with MTurk results

### Quoted Evidence from Source

> We used a 5 (background) × 4 (density) factorial design with 3 replications, resulting in 60 trials (HITs) per task.

> Subjects were paid \0.02 per HIT.

> Adjust the grid so that it is as light as possible while still being usably perceptible.

<a name="experiment-2-results-and-discussion"></a>
## Experiment 2 — Results and Discussion

*Section: exp_2*

### Statistical Approach

Applying analysis of variance, we found a significant effect of plot density ( { [3mF[23m (3,2413) = 3.49, p = 0.015) but not of background intensity ( F (4,2413) = 0.44, p = 0.779) 


### Key Findings

#### Plot density had a significant effect on alpha values

- **Test:** ANOVA
- **Effect type:** main effect
- **Variables in model:** plot density, background intensity, alpha values

**Verbatim statistical report:**

> significant effect of plot density ( { [3mF[23m (3,2413) = 3.49, p = 0.015) but not of background intensity ( F (4,2413) = 0.44, p = 0.779) 

- Citations: Stone & Bartram ()

#### Screen resolution had a weak positive correlation with alpha values in task L

- **Test:** correlation
- **Effect type:** correlation
- **Variables in model:** screen resolution, alpha values

**Verbatim statistical report:**

> weak positive correlation ( r (1431) = 0.07, p < 0.01) between alpha values and screen resolution


#### Monitor color depth had a negative correlation with alpha values in task L

- **Test:** correlation
- **Effect type:** correlation
- **Variables in model:** monitor color depth, alpha values

**Verbatim statistical report:**

> negative correlation ( r (1431) = - 0. [3m1[23m76, [3m p[23m < 0.01) between alpha values and monitor color depth


#### Operating system had a significant effect on alpha values

- **Test:** ANOVA
- **Effect type:** main effect
- **Variables in model:** operating system, alpha values

**Verbatim statistical report:**

> significant effect of operating system ( F (1,1391) = 10.24, p < [3m0[23m.[3m001[23m) 



### Authors' Interpretations

- **Crowdsourced results**
  > we surmise that crowdsourced results may be more representative of web users than a single laboratory display.

- **Alpha values in task D**
  > Alpha values for task D have a much higher variance than those of task L, again consistent with past results.

- **Screen resolution and alpha values**
  > Thus as the resolution increased, users tended to make the (likely thinner) gridlines slightly darker.

- **Monitor color depth and alpha values**
  > subjects tended to select lighter alphas on displays with greater color resolution, presumably due to better contrast.

- **Operating system and alpha values**
  > The darker alpha values for Mac OS X prior to 10.6 (220 responses) versus other operating systems (1211 responses) are consistent with a more “washed-out” monitor gamma of 1.8, indicating that the User-Agent field provides some predictive power.


### Authors' Stated Links to Their Own Predictions

- **Plot density effect**
  > consistent with Stone & Bartram’s findings.
  - Citations: Stone & Bartram ()
- **Alpha values in task D**
  > Alpha values for task D have a much higher variance than those of task L, again consistent with past results.






### Missing or Unclear (Non-Statistical)

- Reason for expiration of HITs on MTurk for task D
- Specific criteria for omitting results based on alpha values


### Citations Referenced

- **Stone & Bartram ()** — consistent with Stone & Bartram’s findings

<a name="experiment-3-introduction"></a>
## Experiment 3 — Introduction

*Section: exp_3*

### Rationale for This Experiment

To assess whether crowdsourcing can be used to study variations in chart sizing and gridline spacing, addressing a design variable (visualization size) that is difficult to control in online settings.


### Relation to Prior Experiments

This experiment extends earlier work by examining chart size and gridline spacing, building on prior experiments that explored qualification tasks, compensation, and basic graphical perception replication.


### Specific Predictions

- **chart size effect on accuracy**
  > We investigated the effects of chart size and gridline spacing on the accuracy of value comparisons in a chart.

- **gridline spacing effect on accuracy**
  > We investigated the effects of chart size and gridline spacing on the accuracy of value comparisons in a chart.


### Theoretical Refinements (relative to paper-level intro)

- **crowdsourcing limitation of physical display control**
  > While pixel size can easily be varied, the subjects’ physical display size, resolution, and viewing distance can not be measured reliably.

- **optimal chart sizing for speed and accuracy**
  > Heer et al.’s study ... found that as chart heights were decreased ... subjects initially responded more quickly without diminished accuracy, implying that there are optimal sizes that maximize the speed and accuracy of graphical perception.
  - Citations: Heer et al. (12)


### New Elements Introduced

- Manipulation of chart height (pixel size) beyond previously tested ranges
- Introduction of gridline spacing as an experimental variable
- Measurement of accuracy in value comparison tasks


### Constraints Addressed

- Addresses the limitation of uncontrolled physical display characteristics in crowdsourced studies



### Citations Referenced

- **Heer et al. (12)** — timeseries visualizations study on chart height effects

<a name="experiment-3-methods"></a>
## Experiment 3 — Methods

*Section: exp_3*

### Participants

- **N:** 24
- **Recruitment:** Mechanical Turk
- **Compensation:** $0.02 per HIT (first run), $0.04 per HIT (second run)
- **Testing context:** online, individual participants via MTurk

### Design

**Design statement:** 2 (chart type: bar vs. line) × 3 (height: 40, 80, 160 pixels) × 4 (gridline spacing: 10, 20, 50, 100 units) within-subjects factorial design with three replications.

**Predictors:**

- **chart type**
  - Levels: bar chart, line chart
  - Manipulation: within-subjects
  - Factor type: nominal
- **chart height**
  - Levels: 40 pixels, 80 pixels, 160 pixels
  - Manipulation: within-subjects
  - Factor type: ordinal
- **gridline spacing**
  - Levels: 10 units, 20 units, 50 units, 100 units
  - Manipulation: within-subjects
  - Factor type: ordinal

**Counterbalancing:** not reported

### Outcome Measures

- **estimation error:** |judged difference - true difference|

### Materials

- **Description:** Charts (bar or line) displaying 12 labeled values (A-L) on a 0-100 unit range; values D and I are the compared elements.
- **Source:** created for the experiment (adapted from Heer et al.)
- **Stimulus pool size:** 72 trials in first run, 48 trials in second run
- **Stimuli presented per participant:** 72 per participant in run 3A; 48 per participant in run 3B
- **Additional details:**
  - chart heights: 40, 80, 160 (first run) and 160, 320 pixels (second run)
  - gridlines drawn at intervals of 10, 20, 50, or 100 units

### Procedure

**Ordered steps:**

1. Qualification task with multiple-choice variants of one bar chart and one line chart (80 pixels tall)
2. Present a chart
3. Participant indicates which marked element (left or right) is smaller
4. Participant estimates the difference between the two values
5. Record estimation error

- **Apparatus:** Mechanical Turk platform; web-based presentation
- **Experimenter presence:** remote (online)
- **Presentation format:** factorial trials (order not specified, likely randomized)
- **Stimulus timing:** not reported

**Verbatim instructions (as quoted in the paper):**

> be as accurate as possible while making a “quick visual judgment.”


### Preregistration and Analysis Plan

- **Preregistration:** not reported


### Author-Provided Rationale for Methodological Choices

- Chosen error measure to facilitate comparison with Heer et al.
- Increased payment in second run to encourage participation

### Missing or Unclear

- Power analysis not reported
- Exclusion criteria not stated
- Participant demographics (age, gender, education) not provided
- Exact randomization or ordering scheme not described
- Counterbalancing details absent
- Stimulus timing (duration, ISI) not reported
- Session duration not reported
- Apparatus details beyond MTurk not specified
- Pre-registration status not mentioned
- Detailed data analysis plan not provided

### Citations Referenced in This Section

- **Heer et al. (2010)** — comparison of error measure and stimulus examples (c.f., [12])

### Quoted Evidence from Source

> We used a 2 (chart) × 3 (height) × 4 (gridline spacing) factorial design with 3 replications, for a total of 72 trials (HITs).

> We requested N=24 assignments and paid \0.02 per HIT.

> Subjects were instructed to be as accurate as possible while making a “quick visual judgment.”

<a name="experiment-3-results-and-discussion"></a>
## Experiment 3 — Results and Discussion

*Section: exp_3*

### Statistical Approach

We analyzed a total of 2,880 responses from the two experimental runs. We omitted 46 responses (1.60%) with error > 40. We then ran an ANOVA on the error results. We found statistically significant effects for chart height, gridline spacing, and an interaction of height and spacing. Using Bonferroni-corrected post-hoc tests, we found that charts 40 pixels tall resulted in significantly more error, but found no significant difference between the other heights. We also analyzed subject performance and experimental costs across our experiments, investigating subject overlap, task completion rates, quality of results, and the money and time costs of running studies on Mechanical Turk.


### Key Findings

#### Chart height significantly affected error rates

- **Test:** ANOVA
- **Effect type:** main effect
- **Variables in model:** chart height, gridline spacing, error

**Verbatim statistical report:**

> F (3,2802) = 14.16, p < 0.001


#### Gridline spacing significantly affected error rates

- **Test:** ANOVA
- **Effect type:** main effect
- **Variables in model:** chart height, gridline spacing, error

**Verbatim statistical report:**

> F (3,2802) = 31.98, p < 0.001


#### Interaction between chart height and gridline spacing significantly affected error rates

- **Test:** ANOVA
- **Effect type:** interaction
- **Variables in model:** chart height, gridline spacing, error

**Verbatim statistical report:**

> F (9,2802) = 2.11, p < 0.026


#### Charts 40 pixels tall resulted in significantly more error compared to other heights

- **Test:** Bonferroni-corrected post-hoc tests
- **Effect type:** post-hoc comparison
- **Variables in model:** chart height, error

**Verbatim statistical report:**

> p < 0.001 in all cases


#### No significant difference in error rates between chart heights of 80, 120, and 160 pixels

- **Test:** Bonferroni-corrected post-hoc tests
- **Effect type:** post-hoc comparison
- **Variables in model:** chart height, error

**Verbatim statistical report:**

> not significant


#### No significant difference in error rates between 10 and 20 gridlines

- **Test:** Bonferroni-corrected post-hoc tests
- **Effect type:** post-hoc comparison
- **Variables in model:** gridline spacing, error

**Verbatim statistical report:**

> p = 0.887


#### No significant difference in error rates between 50 and 100 gridlines

- **Test:** Bonferroni-corrected post-hoc tests
- **Effect type:** post-hoc comparison
- **Variables in model:** gridline spacing, error

**Verbatim statistical report:**

> p = 0.905


#### Subjects spent an average of 5 extra seconds adjusting alpha contrast on dense plots

- **Test:** ANOVA
- **Effect type:** main effect
- **Variables in model:** alpha contrast, time spent

**Verbatim statistical report:**

> F (3,1391) = 3.25, p = 0.021

**Verbatim descriptives:**

> median response time was 42s (µ=54s, σ=41s)


#### Reward level significantly affected the elapsed time from experiment launch to HIT completion

- **Test:** ANOVA
- **Effect type:** main effect
- **Variables in model:** reward level, elapsed time

**Verbatim statistical report:**

> F (1,11521) = 281.28, p < 0.001

**Verbatim descriptives:**

> elapsed time averaged 0.8 days in the high-reward case and 1.9 days in the low-reward case


#### Reward level significantly affected the elapsed time for HIT completion in Experiment 3A and 3B

- **Test:** ANOVA
- **Effect type:** main effect
- **Variables in model:** reward level, elapsed time

**Verbatim statistical report:**

> F (1,1136) = 1035.56, p < 0.001

**Verbatim descriptives:**

> Turkers completed more tasks when paid more


#### Reward level did not significantly affect the time spent completing an individual HIT

- **Test:** ANOVA
- **Effect type:** main effect
- **Variables in model:** reward level, time spent per HIT

**Verbatim statistical report:**

> F (1,1136) = 0.08, p = 0.778


#### Reward level had a small but significant effect on accuracy

- **Test:** ANOVA
- **Effect type:** main effect
- **Variables in model:** reward level, accuracy

**Verbatim statistical report:**

> F (1,1136) = 7.79, p < 0.005

**Verbatim descriptives:**

> Turkers were less accurate (∆µ = 1.4 units) when paid more



### Authors' Interpretations

- **Chart height and accuracy**
  > The results confirm our hypothesis that accuracy plateaus as chart heights increase, and suggest little benefit for increasing chart height beyond 80 pixels when using a 0-100 scale. This size roughly coincides with the point at which the pixel and data resolutions match.

- **Gridline spacing and accuracy**
  > The results suggest that gridlines be separated by at least 8 pixels.

- **Subject overlap across studies**
  > For any given study, an average of 1/3 of subjects also participated in another experiment.

- **Turker completion patterns**
  > It is these 'streakers' who do the lion’s share of the work: almost half of all trials (45.7%) were completed by the 52 Turkers with an average completion rate of 95% or higher.

- **Quality of Turker results**
  > Overall, we found the quality of Turkers’ responses to be high: rejected outliers constituted only 0.75% of responses.

- **Fine-grained timing data**
  > Despite these limitations, significant effects due to time may still be found in the data.

- **Reward level and study completion time**
  > Our results corroborate those of Mason & Watts [23]: paying more does not substantially affect the quality of results, but does increase the rate of HIT completion. By raising the reward, experimenters can decrease the time to results.
  - Citations: Mason & Watts (2009)
- **Cost savings of crowdsourcing**
  > Thus our crowdsourced studies realized a cost savings factor of 6. Had we run all crowdsourced experiments with a $0.02 reward, this increases to a factor of 9 and thus order of magnitude savings are possible.

- **Benefits of crowdsourcing**
  > Crowdsourcing also provides opportunities beyond simple cost-cutting. Mechanical Turk largely eliminates recruiting effort, makes it easy to extend or modify a study, and automates administration. These result in substantial savings of time and effort: in just a few days (for Exp.3B, a single day) we were able to run studies that normally would have taken two weeks due to recruiting and scheduling. Moreover, crowdsourcing can scale to large samples that would otherwise be prohibitively large (e.g.,550 Turkers in [8]), greatly expanding the space of feasible study designs.
  - Citations: Unknown (Unknown)
- **Rectangular area judgment experiment**
  > This result suggests that the 'squarified' optimization objective of leading treemap algorithms [3,35] may rest on tenuous perceptual footing, and that viewers benefit from the inability of the algorithm to achieve its objective.
  - Citations: Unknown (Unknown); Unknown (Unknown)
- **Chart height and gridline spacing experiment**
  > Our chart height and gridline spacing experiment (3) suggests optimized parameters for displaying charts on the web: gridlines should be spaced at least 8 pixels apart and increasing chart heights beyond 80 pixels provides little accuracy benefit on a 0-100 scale.

- **Use of Mechanical Turk for conducting web-based experiments**
  > Experimenters can expect significant subject overlap when running simultaneous studies, and unreliable response times when using the standard HIT interface. By using qualification tasks and verifiable questions, one can increase the likelihood of high-quality responses. As higher rewards led to faster completion rates with little substantive difference in response quality, experimenters can use payment level to influence study completion time.

- **Benefits of crowdsourcing over laboratory experiments**
  > We found that crowdsourcing can provide up to an order of magnitude cost reduction. Such savings could be reinvested in more subjects or more conditions. For constant dollars, we might run better experiments. We realized a faster time to completion. This is separate from cost and can also be used to enrich experimental design, especially when experiments are run in stages. We can also gain access to wider populations [13]. Many experiments are done on college undergraduates due to the difficulty of recruiting wider populations. Crowdsourcing reduces this cost.
  - Citations: Unknown (Unknown)
- **Future research on crowdsourcing**
  > Future research is needed to develop better tools for crowdsourced experimentation. The facilities for conducting user studies on Mechanical Turk are still rudimentary. Dynamic task generation and easier access control would help researchers conduct adaptive studies, enforce between-subjects designs, and prevent subject overlap across experiments.


### Authors' Stated Links to Their Own Predictions

- **Chart height and accuracy prediction**
  > The results confirm our hypothesis that accuracy plateaus as chart heights increase, and suggest little benefit for increasing chart height beyond 80 pixels when using a 0-100 scale.


### Anomalous or Unexpected Results (as characterized by authors)

- Error increased steeply in charts with a height of 40 pixels and gridline spacing of 10 units. Presumably the dense packing of gridlines impedes accurate tracing to their labels.



### Limitations Stated by Authors

- Although we found crowdsourcing to provide high-quality responses, the standard MTurk interface makes it difficult to collect fine-grained timing data. In a laboratory setting, we estimate that the trials in our experiments take a few seconds on average. In our crowdsourced studies, however, the average timing data was significantly higher. Rather than a few seconds per trial, the median response time was 42s (µ=54s, σ=41s). We observed a minimum time of 5 seconds, yet many responses took multiple minutes. There is simply not enough control: it is unclear how much time is due to page loading, scrolling, user inattention, and response submission.
- Despite these limitations, significant effects due to time may still be found in the data. In experiment 2L, subjects spent an average of 5 extra seconds adjusting alpha contrast on dense plots (F (3,1391) = 3.25, p = 0.021). However, due to the inordinately high means and large variation, we forego making any predictions or recommendations based on such results.
- Our own misestimation of the average response time led us to compensate Turkers at decidedly less than minimum wage.
- Some studies, particularly those dependent on physical or environmental context (e.g., [24,36]) are simply ill-suited to the web. Crowdsourcing results might also be insensitive to factors such as color blindness or limited visual acuity.


### Preview of Next Experiment

Future work may lead to improved layout algorithms. Our results help characterize the use of Mechanical Turk for conducting web-based experiments. Experimenters can expect significant subject overlap when running simultaneous studies, and unreliable response times when using the standard HIT interface. By using qualification tasks and verifiable questions, one can increase the likelihood of high-quality responses. As higher rewards led to faster completion rates with little substantive difference in response quality, experimenters can use payment level to influence study completion time. To facilitate replication, we recommend that experimenters describe qualification tasks and compensation rate when publishing the results of crowdsourced studies. Future research is needed to develop better tools for crowdsourced experimentation. The facilities for conducting user studies on Mechanical Turk are still rudimentary. Dynamic task generation and easier access control would help researchers conduct adaptive studies, enforce between-subjects designs, and prevent subject overlap across experiments. By integrating crowdsourcing tools with web-based experiment design tools [20], an entire class of user studies may be subject to cheap, scalable web-based design and deployment. Moreover, by archiving and disseminating HIT definitions, such tools might also greatly facilitate study replication, comparison, or modification. In this spirit, all materials used for the studies in this paper can be downloaded from http://hci.stanford.edu/gp/chi10.zip.


### Missing or Unclear (Non-Statistical)

- The authors do not provide specific details on the qualification tasks used to ensure subject understanding.
- The authors do not provide specific details on the verifiable questions used to dissuade gaming.
- The authors do not provide specific details on the dynamic task generation and easier access control tools that could be developed for crowdsourced experimentation.


### Citations Referenced

- **Unknown (Unknown)** — cited for treemap algorithms
- **Unknown (Unknown)** — cited for treemap algorithms
- **Mason & Watts (2009)** — cited for corroborating results on reward level and study completion time
- **Unknown (Unknown)** — cited for wider populations in crowdsourcing
- **Unknown (Unknown)** — cited for large sample size in crowdsourcing
- **Unknown (Unknown)** — cited for physical or environmental context studies
- **Unknown (Unknown)** — cited for physical or environmental context studies
- **Unknown (Unknown)** — cited for web-based experiment design tools

<a name="general-discussion"></a>
## General Discussion

*Not available for this paper.*

<a name="critique"></a>
## Critique

*Paper: heer-and-bostock-2010-crowdsourcing-graphical-perception--using-mechanical-turk-to-assess-visualization-design*

### Overall Assessment

The paper suffers from several high‑severity methodological and statistical shortcomings, most notably the incomplete reporting of factorial interaction effects in Experiment 3, which undermines the validity of its central claims. While the theoretical framing is articulated, the alignment between the measured outcomes and the intended constructs is ambiguous, and the evidentiary support is weakened by contradictory findings and insufficient effect size reporting. Moreover, the lack of power analyses, participant demographics, and correction for multiple comparisons raises concerns about the rigor and robustness of the analyses. Consequently, the study’s scholarly standing is compromised by these pervasive issues.



### 1. Design–Theory Alignment

- **The outcome measure of "estimated percentage" conflates proportion estimation with absolute area perception, making it unclear whether the task isolates the theoretical construct of area perception.**
  - Severity: **moderate**
  - Justification: The theoretical claim concerns graphical perception of visual encodings (e.g., area vs. angle). By asking participants to report a percentage, the task mixes proportion judgment with absolute area discrimination, which may engage additional cognitive processes not captured by the theory. This limits the ability to attribute observed effects directly to the intended perceptual construct.
  - Evidence:
    - `methods`/`exp_1A` — field `outcome_measures`: free‑text estimate of the smaller value as a percentage of the larger value
    - `results_and_discussion`/`exp_1A` — field `key_findings`: findings are interpreted in terms of psychophysical theory about area and angle encodings


### 2. Evidence–Theory Alignment

- **The authors claim overall validity of the crowdsourced study despite a key finding that contradicts the theoretical prediction that angle encoding should be less accurate than length encoding.**
  - Severity: **moderate**
  - Justification: The paper advances a theoretical claim that crowdsourced perception aligns with established psychophysical rankings. However, a central prediction (angle < length) is falsified and the authors downplay this inconsistency while still asserting overall validity. This overreach weakens the alignment between evidence and theory.
  - Evidence:
    - `results_and_discussion`/`exp_1A` — field `key_findings`: Angle does not perform worse than length, contrary to psychophysical theory, yet authors interpret the results as supporting the theory overall.
    - `results_and_discussion`/`exp_1A` — field `authors_interpretations`: Authors state "The new results match expectations... Theory also suggests that angle should perform worse than length, but the results do not support this." but still conclude the study validates the crowdsourced approach.

- **In Experiment 1B the authors assert that rectangular area judgments match circular area judgments, yet they also report that aspect ratio = 1 (the most square) yields the worst performance, which contradicts the hypothesis that extreme aspect ratios impair judgments.**
  - Severity: **moderate**
  - Justification: The authors conclude that the hypothesis about similarity to circular judgments is confirmed, yet the unexpected worst performance at the neutral aspect ratio directly opposes the predicted pattern. The discussion does not reconcile this discrepancy, leading to an overstated claim of theoretical support.
  - Evidence:
    - `results_and_discussion`/`exp_1B` — field `key_findings`: Finding that aspect ratio = 1 exhibited the worst performance, surprising given the hypothesis that extreme (non‑square) ratios would hamper judgments.
    - `exp_introduction`/`exp_1B` — field `specific_predictions`: Hypothesis predicts performance similar to circular case but impacted by varying aspect ratios, implying that extreme ratios would be detrimental.

- **The paper generalizes that crowdsourced perception experiments are viable for visualization design broadly, despite limited evidence confined to specific encodings and tasks, and without addressing the lack of control over display conditions.**
  - Severity: **minor**
  - Justification: While the empirical work supports viability for a narrow set of visual variables, the authors extrapolate to the entire domain of visualization design without empirical evidence for many other variables (e.g., color, motion). This overgeneralization weakens the alignment between the presented evidence and the broad theoretical claim.
  - Evidence:
    - `abstract` — field `verbatim_quote`: Authors state "Our results demonstrate that crowdsourced perception experiments are viable and contribute new insights for visualization design."
    - `introduction` — field `research_gap`: Acknowledges loss of control over display, lighting, viewing distance, which limits experiment scope, yet the conclusion extends viability to all visualization design.


### 3. Internal Consistency

- **The paper’s introduction claims that compensation level influences speed but not accuracy, yet Experiment 3 reports a small but significant decrease in accuracy when pay is higher.**
  - Severity: **moderate**
  - Justification: The stated mechanistic claim in the introduction suggests that increasing compensation should not affect response accuracy, only the rate of data collection. However, the results from Experiment 3 contradict this by showing a statistically significant reduction in accuracy under higher pay conditions. This inconsistency weakens the internal coherence between the paper’s theoretical expectations and its empirical findings.
  - Evidence:
    - `introduction` — field `mechanistic_claims`: higher pay speeds data collection
    - `results_and_discussion`/`exp_3` — field `key_findings`: Reward level had a small but significant effect on accuracy (F (1,1136) = 7.79, p < 0.005); Turkers were less accurate when paid more


### 4. Alternative Accounts

- **The paper raises the traditional laboratory‑based perception theory as an alternative but does not provide a direct empirical test distinguishing it from the crowdsourced approach, leaving the core claim of equivalence under‑examined.**
  - Severity: **moderate**
  - Justification: While the authors acknowledge that loss of environmental control could limit experiment scope, they do not empirically compare performance under controlled lab conditions versus the crowdsourced setting. Without such a comparison, the alternative laboratory‑based account remains unaddressed, weakening the claim that crowdsourcing yields comparable perception measurements.
  - Evidence:
    - `introduction` — field `alternative_theories`: Lists "laboratory‑based perception theory" as a competing account that emphasizes strict control over display and lighting conditions.
    - `results_and_discussion`/`exp_1A` — field `authors_interpretations`: Authors claim the preserved ranking of judgment types supports the validity of the crowdsourced study, but no analysis isolates the effect of uncontrolled environmental variables versus the laboratory theory.


### 5. Statistical Completeness

- **The 2 × 9 factorial design in Experiment 1B should include a test of the interaction between display type and aspect ratio, but the results only report main effects and omit any interaction analysis.**
  - Severity: **moderate**
  - Justification: In a 2 × 9 ANOVA, the complete set of effects includes two main effects and one interaction. Omitting the interaction leaves the statistical reporting incomplete, preventing assessment of whether the effect of aspect ratio depends on display type.
  - Evidence:
    - `methods`/`exp_1b` — field `design_statement`: 2 (display: T8 vs. T9) x 9 (aspect ratio levels) within-subjects factorial design.
    - `results_and_discussion`/`exp_1b` — field `key_findings`: Reports main effects of display type and aspect ratio, but no interaction effect.

- **The 5 × 4 factorial design in Experiment 2 should report the interaction between background and density, yet only main effects (plot density) and several correlations are presented.**
  - Severity: **moderate**
  - Justification: A full 5 × 4 ANOVA requires reporting two main effects and the background × density interaction. The absence of any interaction test means the analysis is incomplete.
  - Evidence:
    - `methods`/`exp_2` — field `design_statement`: 5 (background) × 4 (density) within-subjects factorial design.
    - `results_and_discussion`/`exp_2` — field `key_findings`: Reports a main effect of plot density and no effect of background intensity, but no interaction analysis.

- **Experiment 3’s 2 × 3 × 4 design lacks reporting of the main effect of chart type, two‑way interactions involving chart type, and the three‑way interaction, despite the design necessitating these analyses.**
  - Severity: **high**
  - Justification: A 2 × 3 × 4 ANOVA entails three main effects, three two‑way interactions, and one three‑way interaction. Omitting five of these effects leaves the statistical reporting substantially incomplete and hampers interpretation of how chart type influences perception.
  - Evidence:
    - `methods`/`exp_3` — field `design_statement`: 2 (chart type) × 3 (height) × 4 (gridline spacing) within-subjects factorial design.
    - `results_and_discussion`/`exp_3` — field `key_findings`: Reports main effects for chart height and gridline spacing, and an interaction between height and spacing, but no mention of chart type main effect, chart type × height, chart type × spacing, or the three‑way interaction.

- **When a significant interaction (height × spacing) is reported in Experiment 3, the paper does not provide simple‑effects analyses or post‑hoc comparisons that isolate the interaction, only separate main‑effect post‑hoc tests.**
  - Severity: **moderate**
  - Justification: Standard practice after a significant interaction is to conduct simple‑effects or interaction‑specific post‑hoc tests. Their absence limits insight into how the two factors jointly affect error.
  - Evidence:
    - `results_and_discussion`/`exp_3` — field `key_findings`: Interaction between chart height and gridline spacing reported as significant (F (9,2802) = 2.11, p < 0.026) but subsequent post‑hoc tests address only height or spacing alone.


### 6. Methodological Concerns

- **No power analysis is reported for any of the experiments despite large numbers of conditions and within‑subject designs.**
  - Severity: **moderate**
  - Justification: Without a priori power calculations the study cannot demonstrate that sample sizes are sufficient to detect the hypothesized effects, raising doubts about the reliability of null findings and the precision of reported effects.
  - Evidence:
    - `methods`/`exp_1A` — field `power_analysis`: power_analysis: null
    - `methods`/`exp_1B` — field `power_analysis`: power_analysis: null
    - `methods`/`exp_2` — field `power_analysis`: power_analysis: null
    - `methods`/`exp_3` — field `power_analysis`: power_analysis: null

- **Exclusion criteria and demographic information for participants are absent across all experiments.**
  - Severity: **moderate**
  - Justification: Transparent reporting of who was excluded and the participant characteristics is essential for assessing sample representativeness and for replicability; the lack of such information limits interpretability of the results.
  - Evidence:
    - `methods`/`exp_1A` — field `exclusions`: exclusions: [] (none stated)
    - `methods`/`exp_1A` — field `demographics`: demographics: null
    - `methods`/`exp_1B` — field `exclusions`: exclusions: [] (none stated)
    - `methods`/`exp_1B` — field `demographics`: demographics: null
    - `methods`/`exp_2` — field `exclusions`: exclusions: [] (none stated)
    - `methods`/`exp_2` — field `demographics`: demographics: null
    - `methods`/`exp_3` — field `exclusions`: exclusions: [] (none stated)
    - `methods`/`exp_3` — field `demographics`: demographics: null

- **No preregistration or publicly available analysis plan is mentioned for any of the studies.**
  - Severity: **minor**
  - Justification: Preregistration helps prevent analytic flexibility and p‑hacking; its absence reduces confidence that the reported analyses were not selectively chosen after seeing the data.
  - Evidence:
    - `methods`/`exp_1A` — field `preregistration_status`: preregistration_status: "not reported"
    - `methods`/`exp_1B` — field `preregistration_status`: preregistration_status: "not reported"
    - `methods`/`exp_2` — field `preregistration_status`: preregistration_status: "not reported"
    - `methods`/`exp_3` — field `preregistration_status`: preregistration_status: "not reported"


### 7. Statistical Robustness

- **Effect sizes or confidence intervals are not reported alongside p‑values for the many ANOVA comparisons, limiting assessment of practical significance**
  - Severity: **moderate**
  - Justification: Without effect sizes or confidence intervals, readers cannot gauge whether statistically significant results correspond to meaningful differences in perception. This omission hampers the interpretability and cumulative value of the findings.
  - Evidence:
    - `results_and_discussion`/`exp_1A` — field `key_findings`: All findings are described only with statements like "significantly outperformed" or "significant effect" without any reported η², Cohen's d, or confidence intervals.
    - `results_and_discussion`/`exp_1B` — field `key_findings`: ANOVA results are presented as "p < 0.05" with no accompanying effect size metrics.
    - `results_and_discussion`/`exp_2` — field `key_findings`: Significant main effects of plot density, operating system, etc., are reported without effect size estimates.
    - `results_and_discussion`/`exp_3` — field `key_findings`: Multiple significant ANOVA and post‑hoc results are given (e.g., F (3,2802) = 14.16, p < 0.001) but no η², partial η², or confidence intervals are provided.

- **Multiple hypothesis tests are conducted (e.g., many ANOVAs and post‑hoc comparisons) without any reported correction for family‑wise error rate**
  - Severity: **moderate**
  - Justification: Conducting many statistical tests inflates the chance of Type I errors. Reporting unadjusted p‑values may overstate the evidence for effects, especially when some reported p‑values are only marginally below .05.
  - Evidence:
    - `results_and_discussion`/`exp_1B` — field `key_findings`: Separate ANOVAs for display type, aspect ratio, and their interaction are reported, yet no adjustment (e.g., Bonferroni, Holm) is mentioned.
    - `results_and_discussion`/`exp_2` — field `key_findings`: Four main effects (plot density, background intensity, operating system, etc.) are tested with p‑values but no multiple‑comparison correction is described.
    - `results_and_discussion`/`exp_3` — field `key_findings`: Numerous post‑hoc pairwise tests are performed (e.g., Bonferroni‑corrected tests are mentioned only for some comparisons), yet the overall family of tests across chart height, gridline spacing, reward effects, etc., lacks a clear correction strategy.

- **Marginally significant p‑values (e.g., p = 0.015, p = 0.021) are presented as strong evidence without discussion of their limited robustness**
  - Severity: **minor**
  - Justification: Treating p‑values just below the conventional .05 threshold as definitive evidence can be misleading, particularly when effect sizes are unreported and multiple tests are performed.
  - Evidence:
    - `results_and_discussion`/`exp_2` — field `key_findings`: The effect of plot density is reported as F (3,2413) = 3.49, p = 0.015 and is interpreted as a meaningful result, yet no caution about the modest significance level is offered.
    - `results_and_discussion`/`exp_3` — field `key_findings`: Reward level’s small effect on accuracy is reported with F (1,1136) = 7.79, p < 0.005 and described as “small but significant,” but no discussion of practical relevance or confidence interval is provided.
