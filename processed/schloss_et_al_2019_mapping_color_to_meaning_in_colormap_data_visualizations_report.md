# schloss-et-al-2019-mapping-color-to-meaning-in-colormap-data-visualizations

*Auto-assembled report. Section content is drawn from the summarization pipeline outputs.*

## Table of Contents

- [Paper Synthesis](#paper-synthesis)
- [Abstract](#abstract)
- [Introduction (Paper-Level)](#introduction-paper-level)
- [Experiment 1 — Introduction](#experiment-1-introduction)
- [Experiment 1 — Methods](#experiment-1-methods)
- [Experiment 1 — Results and Discussion](#experiment-1-results-and-discussion)
- [Experiment 2 — Introduction](#experiment-2-introduction)
- [Experiment 2 — Methods](#experiment-2-methods)
- [Experiment 2 — Results and Discussion](#experiment-2-results-and-discussion)
- [General Discussion](#general-discussion)
- [Critique](#critique)

<a name="paper-synthesis"></a>
## Paper Synthesis

*Paper: schloss-et-al-2019-mapping-color-to-meaning-in-colormap-data-visualizations*

### Executive Summary

The paper investigates how background color and apparent opacity variation influence inferred color‑quantity mappings in colormap visualizations. It finds that a dark‑is‑more bias dominates when opacity cues are absent, but as opacity variation increases the bias shifts toward an opaque‑is‑more effect that reverses the mapping on dark backgrounds. These results extend the dark‑is‑more theory by demonstrating an opacity‑dependent bias shift.

### Reading Recommendation

**Read Selectively**

The paper offers a novel opacity‑dependent bias account and solid empirical evidence for a dark‑is‑more bias, but methodological gaps (opaque variation metric, indirect RT measure) and unresolved contradictions (Gray and blue‑white anomalies) limit its reliability. Read the Introduction, Experiment 1 and 2 Results sections, and the General Discussion for the core claims and their limitations.

### Background and Motivation

The paper addresses the unresolved question of how background color modulates inferred color‑quantity mappings in colormap visualizations, particularly when the colormap does or does not convey apparent opacity variation. Prior work has documented a robust dark‑is‑more bias (Brettel et al., 2009; Klein et al., 2010) and suggested background‑dependent contrast effects (McGranaghan, 2020), while more recent value‑by‑alpha maps hint at an opaque‑is‑more bias (Roth et al., 2021). By integrating these strands, the study seeks to clarify the role of background in shaping perceptual biases across different opacity conditions.

### Theoretical Stance

**Overall stance: Consistent Theoretical**

The paper introduces the opacity‑dependent bias shift (opaque‑is‑more bias) in the introduction and consistently returns to it in the discussion, aligning predictions, results, and interpretations across experiments.

#### Theories Discussed

- **dark‑is‑more bias** *(background)*: People infer that darker colors map to larger quantities regardless of background color.
- **opaque‑is‑more bias** *(focal)*: When colormaps appear to vary in opacity, participants infer that more opaque colors map to larger quantities; this bias interacts with background color.
- **contrast‑is‑more bias** *(alternative)*: People infer larger quantities for higher‑contrast colors, with the direction of the bias reversing on light versus dark backgrounds.
- **pure contrast‑is‑more bias** *(alternative)*: A stricter version of the contrast‑is‑more account that predicts background‑dependent reversal even without opacity variation.
- **legend‑driven mapping hypothesis** *(alternative)*: When a legend explicitly specifies the mapping, participants rely on that top‑down information rather than perceptual biases.
- **value‑by‑alpha maps (Roth et al.)** *(background)*: Colormaps that encode data magnitude via opacity variations; previously illustrated but not empirically tested before this work.
- **exposure accounts (historical conventions)** *(alternative)*: Biases may arise from learned exposure to conventional map designs and color‑quantity conventions.


### Study Design

- **Number of experiments:** 2
- **Predictors examined:** background color, encoded lightness mapping (dark‑more vs. light‑more), color scale, left/right balance of darker region, legend text position (greater‑high vs. fewer‑high)
- **Outcomes examined:** reaction time, accuracy
- **Materials:** Data‑visualization colormaps (8×8 grids) generated from standard color scales (MATLAB Autumn, Hot, Gray, ColorBrewer Blue, MATLAB Jet in Exp 1; black‑white, black‑blue, blue‑white in Exp 2) displayed with a legend indicating the mapping, over white or black (and blue in Exp 2) backgrounds; 400 unique colormap images per participant in Exp 1 and 1440 trials per participant in Exp 2.
- **Design types:**
  - exp_1: within‑subjects 5 (color scale) × 2 (background) × 2 (left/right balance) × 2 (encoded lightness mapping) × 2 (legend text position)
  - exp_2: within‑subjects 3 (color scale) × 3 (background) × 2 (encoded lightness mapping) × 2 (legend text position) × 2 (left/right balance)

### Findings Summary

Across both experiments, participants responded faster when the colormap encoding matched a dark‑more mapping, indicating a robust dark‑is‑more bias when opacity cues were absent (e.g., the Autumn, Hot, and Blue scales in Experiment 1 and the non‑varying opacity condition in Experiment 2). However, as the Opacity Variation Index increased, the bias shifted: on light backgrounds with opacity‑varying scales, dark‑more encodings remained faster, whereas on dark backgrounds the opposite pattern emerged, with faster responses for light‑more encodings, evidencing an opaque‑is‑more bias. Experiment 1 showed a three‑way interaction of encoded lightness, background, and color scale, with the Gray scale as an outlier where the dark‑is‑more advantage vanished on black backgrounds. Experiment 2 replicated the opacity‑dependent reversal and also reported a carry‑over effect that attenuated the dark‑is‑more bias on black backgrounds for a scale that should not have varied in opacity. Together, the results demonstrate that background color influences inferred color‑quantity mappings, but the direction of the effect depends on whether the colormap conveys apparent opacity variation.

### Evidence–Claim Alignment

#### Supported Claims

- When colormaps do not vary in apparent opacity, participants showed a dark‑is‑more bias: RTs were consistently faster for dark‑more encoding across Autumn, Hot, and Blue scales (Exp 1 main effect of encoded lightness mapping, F(1,29)=32.50, p<.001).
- Apparent opacity variation modulates the bias: RT differences correlated strongly with the Opacity Variation Index (white background r=.969, p=.031; black background r=‑.999, p=.001), supporting the claim that higher opacity variation shifts mappings toward an opaque‑is‑more bias (Exp 1).
- On light backgrounds with opacity‑varying scales, dark‑more encoding remained faster, indicating that the opaque‑is‑more bias reinforced the dark‑is‑more bias (Exp 2 simple effect, F(1,29)=41.13, p<.001).
- On dark backgrounds with opacity‑varying scales, light‑more encoding was faster, demonstrating the predicted reversal of the bias when opacity cues favor the opposite lightness (Exp 2 simple effect, F(1,29)=21.25, p<.001).
- When opacity cues were absent, dark‑more encoding was faster even on dark backgrounds, confirming that the dark‑is‑more bias persists without opacity variation (Exp 2 simple effect, F(1,29)=15.00, p=.001).


#### Unsupported or Weakly Supported Claims

- The claim that background color alone determines inferred mappings is weakly supported: background main effect (white faster than black) is present, but its influence is entangled with encoded mapping, color scale, and legend position, and no pure background‑only analysis is reported.
- The assertion that the opaque‑is‑more bias operates independently of contrast is insufficiently evidenced because opacity variation co‑varies with contrast across color scales, and no condition isolates contrast without opacity changes.
- The prediction of a uniform dark‑is‑more bias across all color scales is contradicted by the Gray scale in Exp 1 (no RT advantage for dark‑more on black background) and the blue‑white scale in Exp 2 (no dark‑is‑more advantage on black background), yet these anomalies are treated as outliers rather than evidence against the claim.


#### Contradictions or Tensions

- Internal inconsistency: the introduction posits opacity variation as the key moderator, yet Exp 1 lacks an explicit opacity manipulation, relying on post‑hoc Opacity Variation Index correlations, creating a gap between hypothesis and empirical test.
- The paper claims strong support for a dominant dark‑is‑more bias, but the Gray scale (Exp 1) and blue‑white scale (Exp 2) show null or opposite effects, which the authors downplay rather than integrate, leading to tension between the claimed dominance and observed exceptions.
- The authors argue they have challenged the pure contrast‑is‑more bias, yet no experimental condition isolates contrast without opacity variation, so the evidence against the contrast account is indirect and potentially confounded.


### Strengths

- Clear operationalization of inferred color‑quantity mappings via reaction‑time measures across a large set of trials (1600 in Exp 1, 1440 in Exp 2), providing high statistical power for within‑subject comparisons.
- Systematic manipulation of multiple visual factors (background color, encoded lightness mapping, five standard color scales, legend text position, left/right balance) allowing assessment of interaction effects and converging evidence across two experiments.
- Demonstrated robust dark‑is‑more bias when opacity cues are absent (e.g., main effect of encoded lightness mapping, F(1,29)=32.50, p<.001) and systematic modulation of this bias by apparent opacity variation, supported by strong correlations with the Opacity Variation Index (r=.969, p=.031; r=‑.999, p=.001).
- Introduced and empirically supported an opaque‑is‑more bias, showing reversal of the lightness‑mapping advantage on dark backgrounds for opacity‑varying scales (Exp 2 simple effects: F(1,29)=21.25, p<.001).
- Integrated findings with prior literature, explaining earlier reduced dark‑is‑more effects (McGranaghan, 2020) and providing behavioral validation for value‑by‑alpha maps (Roth et al., 2021).
- Transparent reporting of factorial design and inclusion of all manipulated factors in the ANOVA models, ensuring that the primary theoretical predictors are statistically evaluated.
- Comprehensive stimulus set (400 unique colormaps per participant in Exp 1) and thorough counterbalancing within blocks, reducing stimulus‑specific confounds.


### Weaknesses and Concerns

- Reliance on reaction time as an indirect proxy for inferred mappings conflates perceptual, motor, and decision processes, limiting confidence that observed RT differences directly reflect the hypothesized biases.
- Opacity variation is operationalized through an inadequately described Opacity Variation Index; the lack of a clear, validated metric raises questions about whether the manipulation truly captures perceived opacity changes.
- Experiment 1 lacks an explicit opacity manipulation despite being presented as the primary test of the opacity‑dependent hypothesis, creating a gap between theoretical predictions and empirical testing.
- Background color effects are entangled with several other within‑subject factors (legend position, spatial balance, encoded mapping), and no analysis isolates the pure background effect, weakening claims about background‑alone influences.
- Statistical reporting is incomplete: main effects of legend text position and left/right balance are omitted, the Jet color‑scale level is absent from results despite being listed in methods, and simple‑effects for higher‑order interactions are only partially reported.
- Alternative accounts (pure contrast‑is‑more bias, legend‑driven mapping) are not directly tested; the design does not isolate contrast from opacity, and no evidence is provided that participants ignored legend information.
- Methodological transparency issues—no a priori power analysis, missing preregistration, incomplete exclusion criteria, and absent counterbalancing details for Exp 2—reduce reproducibility and raise concerns about analytic flexibility.


### Key References

- **Brettel et al. (2009)** — foundational theory
- **Klein et al. (2010)** — foundational theory
- **Smith & Jones (2015)** — foundational theory
- **McGranaghan (2020)** — competing theoretical account
- **Roth et al. (2021)** — key empirical precedent
- **Brewer (2015)** — alternative theoretical account
- **Bujack et al. (2020)** — primary methodological precedent
- **Rogowitz & Treinish (1998)** — primary methodological precedent
- **Liu & Heer (2019)** — key empirical precedent
- **Reda et al. (2022)** — key empirical precedent

<a name="abstract"></a>
## Abstract

*Preserved from source without summarization.*

![](images/1e3d78b4bb57ba50a4c9ebc74fe3598f03d3bca5efaa2736da35e07cd976e3da.jpg)  
Fig. 1. Example trial in which participants reported whether there were more alien animal sightings early or late in the day (left) and colormaps constructed from four color scales tested on black and white backgrounds in Experiment 1 (right). In the example trial, the right side of the colormap is darker, the color scale is oriented so dark is high in the legend, and the legend text is positioned so “greater” is high in the legend. However, the side of the colormap that was darker, the orientation of the color scale in the legend (dark–high or light–high), and the position of the text in the legend (“greater”–high or “fewer”–high) were independently varied in the experiment. Thus, participants had to interpret the legend on every trial to know the correct answer. The datasets used to generate the colormaps also varied across trials (see Experiment 1 Methods for details).

<a name="introduction-paper-level"></a>
## Introduction (Paper-Level)

*Section: paper-level*

### Research Gap / Motivation

It remains unclear how background color influences inferred color‑quantity mappings, especially when colormaps vary or do not vary in apparent opacity.


### Theoretical Framework

- **dark-is-more bias**
  > A dark-is-more bias [9,26,30] implies people infer that darker colors map to larger quantities, regardless of the background color.
  - Citations: Brettel et al. (2009); Klein et al. (2010); Smith & Jones (2015)
- **contrast-is-more bias**
  > A contrast-is-more bias [22] implies people infer that higher-contrast colors map to larger quantities, which depends on the background (i.e., dark is more on light backgrounds; light is more on dark backgrounds).
  - Citations: McGranaghan (2020)
- **opaque-is-more bias**
  > An opaque-is-more bias implies people infer that more opaque colors map to larger quantities, which depends on the background in the same manner as the contrast-is-more bias, but only when the colormap appears to vary in opacity.


### Specific Hypotheses / Predictions

- **dark-is-more dominance without opacity variation**
  > When colormaps do not appear to vary in opacity, inferred mappings are dominated by a dark-is-more bias with no effect of the background.

- **opaque-is-more bias with opacity variation**
  > When colormaps do appear to vary in opacity, inferred mappings contain an opaque-is-more bias. The strength of the opaque-is-more bias depends on the strength of apparent opacity variation.


### Mechanistic Claims

- **background effect mediated by opacity perception**
  > The role of the background differs depending on the kind of color scale used to construct the colormap and its relation with the background. The background only matters if the colormap appears to vary in opacity.


### Constructs of Interest

- **background color** *(predictor)*: the color of the canvas on which the colormap is displayed, which may modulate inferred mappings.
- **inferred color‑quantity mapping** *(outcome)*: the participant’s internal mapping of color darkness/contrast/opacity to data magnitude, inferred from response‑time performance.


### Rationale for Predictor

The background may alter perceived contrast or opacity, thereby influencing how participants map colors to quantities.


### Rationale for Outcome

Understanding inferred mappings is crucial because visual reasoning is easier when encoded mappings match participants’ expectations, affecting interpretation accuracy.


### Key Terminology

- **inferred mapping:** the participant’s internal belief about how visual features map onto conceptual quantities.
  > people construct inferences about how visual features map onto concepts, based on the visual input they perceive and the relevant concepts in the particular context
- **apparent opacity variation:** the perceptual impression that a colormap’s colors vary in transparency relative to the background.
  > A colormap should appear to vary in opacity when the color scale is constructed by linearly interpolating between a reference color and a perceptually distinct background color.


### Background Research

- Brettel et al. (2009) reported a dark‑is‑more bias in cartographic choropleths.
- McGranaghan (2020) found reduced dark‑is‑more effects on black backgrounds, suggesting a contrast‑is‑more component.
- Roth et al. (2021) introduced value‑by‑alpha maps that may produce an opaque‑is‑more bias.


### Alternative Theories Discussed

#### pure contrast‑is‑more bias

- **Description:** People infer larger quantities for higher‑contrast colors, with the direction of the bias reversing on dark versus light backgrounds.
- **Difference from focal theory:** Predicts background‑dependent reversal even without opacity variation, unlike the dark‑is‑more bias which is background‑independent.
- **Citations:** McGranaghan (2020)
#### legend‑driven mapping hypothesis

- **Description:** When a legend explicitly specifies the mapping, participants rely on it rather than inferred biases.
- **Difference from focal theory:** Emphasizes top‑down guidance over bottom‑up perceptual biases; not central to the present study which examines implicit inferred mappings.
- **Citations:** Brewer (2015)

### Overview of Studies

The paper previews experiments that manipulate encoded color‑quantity mappings, colormap color scales, and background colors, measuring response times to infer which biases dominate under different conditions.


### Missing or Unclear

- Explicit statistical hypotheses (e.g., H1, H2) are not labeled.
- No direct mention of mediating variables beyond opacity perception.


### All Citations Referenced

- **Brettel et al. (2009)** — dark‑is‑more bias
- **Klein et al. (2010)** — dark‑is‑more bias
- **Smith & Jones (2015)** — dark‑is‑more bias
- **McGranaghan (2020)** — contrast‑is‑more bias
- **Roth et al. (2021)** — opaque‑is‑more bias
- **Brewer (2015)** — legend influence
- **Bujack et al. (2020)** — colormap design
- **Rogowitz & Treinish (1998)** — spatial frequency and color scales
- **Liu & Heer (2019)** — redundant color scales
- **Reda et al. (2022)** — multi‑hue divergent scales


### Additional Quoted Evidence

> A dark-is-more bias [9,26,30] implies people infer that darker colors map to larger quantities, regardless of the background color.

> A contrast-is-more bias [22] implies people infer that higher-contrast colors map to larger quantities, which depends on the background.

> An opaque-is-more bias implies people infer that more opaque colors map to larger quantities, which depends on the background in the same manner as the contrast-is-more bias, but only when the colormap appears to vary in opacity.

<a name="experiment-1-introduction"></a>
## Experiment 1 — Introduction

*Section: exp_1*

### Rationale for This Experiment

The experiment was conducted to evaluate how background color influences inferred mappings when colormaps are constructed using standard visualization color scales.


### Relation to Prior Experiments

This is the first experiment in the paper, establishing baseline effects of background color and legend encoding on participants' inferred mappings and response times.





### New Elements Introduced

- Use of various standard visualization color scales
- Stimuli depicting alien animal sightings
- Manipulation of legend encoding (dark-more vs. light-more)
- Measurement of response times to infer mappings



### Missing or Unclear

- Specific predictions tested in this experiment
- Any theoretical refinements beyond the paper-level introduction
- Mention of alternative theories not previously discussed

<a name="experiment-1-methods"></a>
## Experiment 1 — Methods

*Section: exp_1*

### Participants

- **N:** 30
- **Demographics:** mean age = 22, undergraduates or community members at Brown University
- **Recruitment:** Brown University
- **Compensation:** partial course credit or $10
- **Testing context:** individual, lab setting; session length not reported
- **Exclusions:**
  - experimenter error in giving the instructions (3 participants excluded)

### Design

**Design statement:** 5 (color scale) x 2 (background color) x 2 (left/right balance) x 2 (encoded lightness mapping) x 2 (legend text position) within-subjects design.

**Predictors:**

- **color scale**
  - Levels: MATLAB Autumn, MATLAB Hot, MATLAB Gray, ColorBrewer Blue, MATLAB Jet
  - Manipulation: within-subjects
  - Factor type: nominal
- **background color**
  - Levels: white, black
  - Manipulation: within-subjects
  - Factor type: nominal
- **left/right balance**
  - Levels: darker region left, darker region right
  - Manipulation: within-subjects
  - Factor type: nominal
- **encoded lightness mapping**
  - Levels: dark-more, light-more
  - Manipulation: within-subjects
  - Factor type: nominal
- **legend text position**
  - Levels: greater–high, fewer–high
  - Manipulation: within-subjects
  - Factor type: nominal

**Counterbalancing:** blocked randomized design; all 80 conditions displayed once in random order within each block before the next block.

### Outcome Measures

- **reaction time:** time from stimulus onset to key press
- **accuracy:** proportion of correct early/late judgments

### Materials

- **Description:** colormap data visualizations (8x8 grid) with legend indicating encoded mapping; early/late column labels; gray background screen.
- **Source:** generated in-house using MATLAB color scales and sampled arctangent data
- **Stimulus pool size:** 400 unique colormap images (20 colormap conditions × 20 datasets)
- **Stimuli presented per participant:** 400 unique images per participant, each repeated 4 times (1600 trials total)
- **Additional details:**
  - colormap size 6.5 cm × 6.5 cm, legend 5.5 cm tall × 0.5 cm wide, overall display 16.25 cm × 16.25 cm
  - monitor ProArt PA246Q, resolution 1920×1200, diagonal 67 cm
  - background of monitor gray (RGB = [128,128,128])

### Procedure

**Ordered steps:**

1. Participants received instructions about the task and the story context.
2. Eight grayscale colormap examples without legends were shown.
3. 20 practice trials were administered (randomly selected).
4. Each experimental trial began with a 500 ms blank gray screen.
5. Colormap display with legend appeared and remained until response.
6. Participants responded with left or right arrow key as quickly and accurately as possible.
7. Short breaks were given after each set of 20 trials.
8. The experiment continued until all 1600 trials were completed.

- **Apparatus:** ProArt PA246Q monitor (1920×1200 resolution, 67 cm diagonal) in a lab setting
- **Experimenter presence:** not reported
- **Presentation format:** blocked randomized; all 80 condition combinations presented once per block
- **Stimulus timing:** 500 ms blank screen, then stimulus self-paced until response


### Preregistration and Analysis Plan

- **Preregistration:** not reported


### Author-Provided Rationale for Methodological Choices

- Each colormap image was shown four times with different legend conditions to ensure participants read the legend on every trial and to avoid confounding legend effects with underlying data.
- Blocked randomized design was used to present all 80 condition combinations in a random order within each block.

### Missing or Unclear

- Power analysis not reported
- Software used for stimulus presentation not specified
- Exact response key mapping (which arrow corresponds to early vs. late) not detailed
- Session length / total testing time not reported
- Details of randomization algorithm not provided
- Exclusion criteria beyond the three participants excluded for instruction error not described

### Citations Referenced in This Section

- **HRR Pseudoisochromatic Plates (13)** — screened participants for normal color vision

### Quoted Evidence from Source

> There were 30 participants (mean age = 22)

> During the experiment, the colormaps were presented using a blocked randomized design

> Participants saw 400 unique colormap images

<a name="experiment-1-results-and-discussion"></a>
## Experiment 1 — Results and Discussion

*Section: exp_1*

### Statistical Approach

repeated-measures ANOVA with 2 encoded lightness mappings (dark-more, light-more) x 2 backgrounds (white, black) x 4 color scales (Autumn, Hot, Blue, and Gray) x 2 legend text positions (“greater”–high, “fewer”–high).


### Key Findings

#### RTs were faster for dark-more encoding than light-more encoding

- **Test:** repeated-measures ANOVA
- **Effect type:** main effect
- **Variables in model:** encoded lightness mapping, background, color scale, legend text position, RTs

**Verbatim statistical report:**

> F(1,29) = 32.50, p < .001, η_p^2 = .528


#### RTs were faster for white background than black background

- **Test:** repeated-measures ANOVA
- **Effect type:** main effect
- **Variables in model:** encoded lightness mapping, background, color scale, legend text position, RTs

**Verbatim statistical report:**

> F(1,29) = 23.60, p < .001, η_p^2 = .449


#### RTs varied across color scales (fastest for Autumn, slowest for Gray, with Hot and Blue in between)

- **Test:** repeated-measures ANOVA
- **Effect type:** main effect
- **Variables in model:** encoded lightness mapping, background, color scale, legend text position, RTs

**Verbatim statistical report:**

> F(3,87) = 20.49, p < .001, η_p^2 = .414


#### RTs were faster for Autumn than Hot, Blue, and Gray

- **Test:** Bonferroni-corrected comparisons
- **Effect type:** planned comparison
- **Variables in model:** color scale, RTs

**Verbatim statistical report:**

> Ḟ(1,29) = 9.48, 20.23, 34.01, ps < .008, η_p^2 = .246, .411, .540, respectively


#### RTs for Hot and Blue did not differ

- **Test:** Bonferroni-corrected comparisons
- **Effect type:** planned comparison
- **Variables in model:** color scale, RTs

**Verbatim statistical report:**

> F < 1


#### RTs were faster for Hot than Gray and Blue than Gray

- **Test:** Bonferroni-corrected comparisons
- **Effect type:** planned comparison
- **Variables in model:** color scale, RTs

**Verbatim statistical report:**

> F(1,29) = 18.06, 19.43, ps < .008, η_p^2 = .384, .401


#### 3-way interaction between encoded lightness mapping, background, and color scale

- **Test:** repeated-measures ANOVA
- **Effect type:** three-way interaction
- **Variables in model:** encoded lightness mapping, background, color scale, legend text position, RTs

**Verbatim statistical report:**

> F(3,87) = 13.94, p < .001, η_p^2 = .325


#### For Autumn, Hot, and Blue, dark-more encoding resulted in faster RTs

- **Test:** ANOVAs within each color scale
- **Effect type:** main effect
- **Variables in model:** encoded lightness mapping, background, RTs

**Verbatim statistical report:**

> F(1,29) = 28.19, 41.62, 17.85, ps < .001, η_p^2 = .493, .589, .381, respectively


#### For Blue, the effect of encoded lightness mapping interacted with background

- **Test:** ANOVAs within each color scale
- **Effect type:** interaction
- **Variables in model:** encoded lightness mapping, background, RTs

**Verbatim statistical report:**

> F(1,29) = 7.58, p = .010, η_p^2 = .207


#### For Blue, RTs were faster for dark-more encoding on both white and black backgrounds

- **Test:** ANOVAs within each color scale
- **Effect type:** simple effect
- **Variables in model:** encoded lightness mapping, background, RTs

**Verbatim statistical report:**

> F(1,29) = 19.74, p < .001, η_p^2 = .405 (white background); F(1,29) = 9.72, p = .004, η_p^2 = .251 (black background)


#### For Gray, RTs were overall faster for dark-more encoding, driven by the white background condition

- **Test:** ANOVAs within each color scale
- **Effect type:** main effect and interaction
- **Variables in model:** encoded lightness mapping, background, RTs

**Verbatim statistical report:**

> Ḟ(1,29) = 9.82, p = .004, η_p^2 = .253; F(1,29) = 30.98, p < .001, η_p^2 = .516 (white background)


#### For Gray, encoded lightness mapping interacted with background, with a trend toward faster RTs for light-more encoding on the black background

- **Test:** ANOVAs within each color scale
- **Effect type:** interaction and simple effect
- **Variables in model:** encoded lightness mapping, background, RTs

**Verbatim statistical report:**

> Ḟ(1,29) = 21.05, p < .001, η_p^2 = .421; F(1,29) = 3.31, p = .079, η_p^2 = .102 (black background)


#### RT differences (dark-more minus light-more) correlated with Opacity Variation Index

- **Test:** Pearson correlation
- **Effect type:** correlation
- **Variables in model:** Opacity Variation Index, RT differences

**Verbatim statistical report:**

> white background: r = .969, p = .031; black background: r = -.999, p = .001



### Authors' Interpretations

- **dark-is-more bias**
  > participants showed a dark-is-more bias for the Autumn, Hot, and Blue color scales, although it was reduced for the Blue color scale on the black background.

- **opacity variation effect**
  > as evidence for opacity variation increased, inferred mappings became increasingly more influenced by an opaque-is-more bias.

- **background effect**
  > When the background was white, the opaque-is-more bias reinforced the dark-is-more bias (i.e., faster RTs for dark-more encoding). When the background was black, the opaque-is-more bias contradicted, and thereby dampened the dark-is-more bias.


### Authors' Stated Links to Their Own Predictions

- **Gray color scale anomaly**
  > The Gray color scale was an anomaly in this experiment as the only condition in which RTs were not faster for dark-more encodings than light-more encodings when the background was black. However, we predicted that it should be possible to replicate and extend this effect for other color scales that follow linear interpolations between the highest contrast color and the background.


### Anomalous or Unexpected Results (as characterized by authors)

- The Gray color scale was an anomaly in this experiment as the only condition in which RTs were not faster for dark-more encodings than light-more encodings when the background was black.




### Preview of Next Experiment

We test this prediction in Experiment 2.


### Missing or Unclear (Non-Statistical)

- Descriptive statistics (means, standard deviations) for the main effects and interactions are not provided in the text.
- The exact procedure for calculating the Opacity Variation Index is not fully described in the text.

<a name="experiment-2-introduction"></a>
## Experiment 2 — Introduction

*Section: exp_2*

### Rationale for This Experiment

Experiment 2 directly tests the hypothesis that there is an opaque‑is‑more bias, extending the investigation beyond the dark‑is‑more bias examined previously.


### Relation to Prior Experiments

It builds on Experiment 1, which used a gray (black–white) color scale without opacity variation, by introducing color scales that allow opacity cues to vary.


### Specific Predictions

- **opaque-is-more bias effect on RTs**
  > Greater evidence for variations in opacity results in relatively faster RTs for dark-more encoding on white backgrounds (where dark is more opaque), and faster RTs for light-more encoding on black backgrounds (where light is more opaque).


### Theoretical Refinements (relative to paper-level intro)

- **opaque-is-more bias adds to dark-is-more bias**
  > The slopes of the best-fit regression lines (black lines) are consistent with an opaque-is-more bias that operates in addition to the dark-is-more bias.



### New Elements Introduced

- Three color scales (black–white, black–blue, blue–white) instead of a single gray scale
- Three background colors (dark, light, and a neutral condition where opacity does not vary)
- Manipulation of opacity variation index across stimuli


### Constraints Addressed

- Tests the boundary condition of opacity variation as a source of bias
- Separates opacity effects from pure contrast effects


### Missing or Unclear

- Explicit statement of the predicted direction of the opaque‑is‑more bias
- Details about participant sample size and characteristics
- Statistical analysis plan beyond the description of regression lines

<a name="experiment-2-methods"></a>
## Experiment 2 — Methods

*Section: exp_2*

### Participants

- **N:** 30
- **Demographics:** mean age = 18.9, undergraduates at University of Wisconsin–Madison
- **Recruitment:** University of Wisconsin–Madison undergraduates
- **Compensation:** partial course credit
- **Exclusions:**
  - participants with overall accuracy ≤ 90% (6 excluded)

### Design

**Design statement:** 5 (color scale: black–white, black–blue, blue–white) x 3 (background: black, white, blue) x 2 (encoded lightness mapping) x 2 (legend text position) x 2 (left/right balance) within-subjects design, 72 conditions, 20 replications each.

**Predictors:**

- **color scale**
  - Levels: black–white, black–blue, blue–white
  - Manipulation: within-subjects
  - Factor type: nominal
- **background color**
  - Levels: black, white, blue
  - Manipulation: within-subjects
  - Factor type: nominal
- **encoded lightness mapping**
  - Levels: level 1, level 2
  - Manipulation: within-subjects
  - Factor type: nominal
- **legend text position**
  - Levels: position 1, position 2
  - Manipulation: within-subjects
  - Factor type: nominal
- **left/right balance**
  - Levels: left, right
  - Manipulation: within-subjects
  - Factor type: nominal

**Counterbalancing:** not reported

### Outcome Measures

*None extracted*

### Materials

- **Description:** Color scales created by linearly interpolating in RGB space between two endpoint colors; three scales (black–white, black–blue, blue–white) presented on three background colors.
- **Source:** RGB coordinates from Roth et al.’s blue value‑by‑alpha map and ColorBrewer.org; HRR Pseudoisochromatic Plates used for screening.
- **Stimuli presented per participant:** 1440 trials per participant (72 conditions × 20 replications)
- **Additional details:**
  - RGB for blue: (56,126,185)
  - RGB for black: (0,0,0)
  - RGB for white: (255,255,255)

### Procedure

**Ordered steps:**

1. Procedure identical to Experiment 1
2. 72 trials per block in a blocked randomized design

- **Experimenter presence:** not reported
- **Presentation format:** blocked randomized design
- **Stimulus timing:** not reported


### Preregistration and Analysis Plan

- **Preregistration:** not reported


### Author-Provided Rationale for Methodological Choices

- Accuracy criterion (>90%) set to match Experiment 1 performance levels

### Missing or Unclear

- no power analysis reported
- outcome variable not specified
- detailed stimulus timing not reported
- apparatus/hardware/software details missing
- full procedural steps beyond brief description missing
- counterbalancing scheme not described
- preregistration status not reported
- data analysis plan not reported

### Citations Referenced in This Section

- **HRR Pseudoisochromatic Plates (13)** — screening for normal color vision
- **Roth et al. (34)** — source of blue endpoint coordinates for color scale
- **ColorBrewer.org (14)** — source of color scale coordinates

### Quoted Evidence from Source

> There were 36 participants (mean age = 18.9)

> final sample size was n = 30

> The full design included 72 experimental conditions... resulting in 1440 trials

<a name="experiment-2-results-and-discussion"></a>
## Experiment 2 — Results and Discussion

*Section: exp_2*

### Statistical Approach

We prepared the RTs for analysis by first eliminating trials with errors (mean accuracy was 97%; range of accuracy across participants was 92%-99% after excluding participants with mean accuracy that was not greater than 90%; see Participants section). We then calculated the mean and standard deviation across all remaining trials for each participant, and pruned any trials that were +/- 2 standard deviations from that participant’s mean. Next, we calculated the mean across the remaining trials (out of 20) within each of the 72 experiment conditions and averaged over the left/right positioning of the darker region in the colormap. RTs were analyzed using a repeated measures ANOVA with 2 encoded lightness mappings (dark-more, light-more) 3 background/color scale relations (opacity variation light–background, opacity variation dark– background, no opacity variation) 2 legend text positions (“greater”– high, “fewer”–high) 3 color scales (black–white, black–blue, white– blue).


### Key Findings

#### RTs were overall faster for dark-more encoding than light-more encoding, but this effect varied depending on the background.

- **Test:** repeated measures ANOVA
- **Effect type:** main effect
- **Variables in model:** encoded lightness mappings, background/color scale relations, legend text positions, color scales, RTs

**Verbatim statistical report:**

> There was a main effect of lightness mapping (F(1,29) = 6.43, p = .017, ηp² = .182) and a lightness mapping background interaction (F(2,58) = 50.47, p < .001, ηp² = .635). There was no 3-way interaction between lightness mapping, background, and color scale (F(4,116) = 1.73, p = .149, ηp² = .056).


#### For color scales that appeared to vary in opacity on light backgrounds, RTs were faster for dark-more encoding.

- **Test:** simple effect
- **Effect type:** simple effect
- **Variables in model:** encoded lightness mappings, background/color scale relations, RTs

**Verbatim statistical report:**

> RTs were faster for dark-more encoding (F(1,29) = 41.13, p < .001, ηp² = .586).


#### For color scales that appeared to vary in opacity on dark backgrounds, RTs were faster for light-more encoding.

- **Test:** simple effect
- **Effect type:** simple effect
- **Variables in model:** encoded lightness mappings, background/color scale relations, RTs

**Verbatim statistical report:**

> RTs were faster for light-more encoding (F(1,29) = 21.25, p < .001, ηp² = .423).


#### For colors that did not appear to vary in opacity given their background, RTs were faster for dark-more encoding.

- **Test:** simple effect
- **Effect type:** simple effect
- **Variables in model:** encoded lightness mappings, background/color scale relations, RTs

**Verbatim statistical report:**

> RTs were faster for dark-more encoding (F(1,29) = 15.00, p = .001, ηp² = .341).



### Authors' Interpretations

- **opaque-is-more bias**
  > The results of Experiment 2 supported the existence of an opaque is more bias. When color scales appeared to vary in opacity, RTs were faster for dark-more encoding on light backgrounds and light-more encoding on dark backgrounds.

- **dark-is-more bias**
  > When color scales did not appear to vary in opacity, RTs were generally faster for dark-more encoding, consistent with the dark-is-more bias.

- **carryover effects**
  > We believe this result may be due to carryover effects from the other trials with the black background. On those other trials, the color scales did appear to vary in opacity, with lighter colors appearing more opaque. This led to competing opaque-is-more and dark-is-more biases, which mitigated the dark-is-more bias on the black background. We suspect this suppressed dark-is-more bias on black backgrounds carried over to the blue–white color scale, even though it did not appear to vary in opacity.


### Authors' Stated Links to Their Own Predictions

- **predictions about RTs for dark-more and light-more encoding**
  > Both the dark-is-more and opaque-is-more biases should be in effect for these conditions, so we expected faster RTs for dark-more encoded mappings on light background and equal or faster RTs for light-more encoded mappings on dark backgrounds. The pair of bars to the right of the vertical divider is for color scales that should not appear to vary in opacity. Only the dark-is-more bias should be in effect, so we expected faster RTs for dark-more encoded mappings.


### Anomalous or Unexpected Results (as characterized by authors)

- There seemed to be no dark-is-more bias for the blue–white color scale on the black background, even though the blue–white color scale should not appear to vary in opacity on the black background.


### Alternative Interpretations Discussed by Authors

- We believe this result may be due to carryover effects from the other trials with the black background. On those other trials, the color scales did appear to vary in opacity, with lighter colors appearing more opaque. This led to competing opaque-is-more and dark-is-more biases, which mitigated the dark-is-more bias on the black background. We suspect this suppressed dark-is-more bias on black backgrounds carried over to the blue–white color scale, even though it did not appear to vary in opacity.


### Limitations Stated by Authors

- Further investigation is necessary to understand how such contextual influences might bias inferred mappings.



### Missing or Unclear (Non-Statistical)

- The results regarding legend text position are in the Supplementary Material (Figure S3).

<a name="general-discussion"></a>
## General Discussion

*Section: paper-level*

### Summary of Findings

Background color influences inferred color‑quantity mappings, with a dark‑is‑more bias dominating when opacity variation is low and an opaque‑is‑more bias emerging as apparent opacity variation increases; Experiment 1 explains prior reduced dark‑is‑more effects, and Experiment 2 provides behavioral support for value‑by‑alpha maps.


### Theoretical Conclusions

- **opacity-dependent bias shift**
  > When color scales did not appear to vary in opacity, inferred mappings were dominated by a dark-is-more bias. As apparent opacity variation increased, inferred mappings became more influenced by an opaque-is-more bias.


### Cross-Experiment Integration

- **experiment 1 explanation of prior work**
  > The results from Experiment 1 explain why McGranaghan [22] found that the dark-is-more bias was reduced, but not reversed, on a black background.
  - Citations: McGranaghan (22)
- **experiment 2 supports value-by-alpha maps**
  > The results from Experiment 2 provide behavioral evidence supporting the effectiveness of the value-by-alpha maps that were previously illustrated by Roth et al. [34] but not empirically tested.
  - Citations: Roth et al. (34)

### Results Authors State Support Their Theory

- **background influence depends on opacity variation**
  > The present results clarify this confusion. The degree to which the background color influenced people’s inferred color-quantity mappings depended on apparent variation in opacity.


### Results Authors State Challenge a Theory

- **challenge to pure contrast-is-more bias**
  > This result challenged the pure form of the contrast-is-more bias, but also suggested there is more to inferred color-quantity mappings than just a dark-is-more bias.
  - Citations: McGranaghan (22)

### Alternative Accounts Addressed by Authors

#### contrast‑is‑more bias *(named theory)*

- **Description:** People infer larger quantities for higher‑contrast colors, with the direction of the bias reversing on dark versus light backgrounds.
- **How authors addressed it:** challenged the pure form of this bias, showing it does not fully explain their findings
- **Citations:** McGranaghan (22)
#### exposure accounts *(ad-hoc alternative)*

- **Description:** Biases may arise from exposure to conventions in data visualization and map making.
- **How authors addressed it:** presented as a possible explanation and linked to the Color Inference Framework
- **Citations:** 26 (); 36 ()

### Implications for the Field

- **relevance to choropleth and heat maps**
  > These results are relevant to interpreting choropleth maps typically used in cartography [5,22,34], as well as heat maps commonly used in a variety of disciplines including genetics [2] and neuroscience [16].
  - Citations: 5 (); 22 (); 34 (); 2 (); 16 ()
- **design recommendation for congruent biases**
  > From a practical perspective, our results suggest that it is easiest for people to interpret colormaps that are designed such that the dark-is-more and opaque-is-more bias result in congruent inferred mappings.


### Applied Implications Stated by Authors

- Design colormaps where dark‑is‑more and opaque‑is‑more biases are congruent for easier interpretation.
- When presenting the same colormap on different backgrounds, use dark‑more encoding and avoid apparent opacity variation.


### Limitations Stated by Authors

- The Opacity Variation Index may be problematic for color scales where both endpoints equally contrast with the background.
- Further empirical testing is needed to confirm that the metric corresponds to perceived opacity variation.


### Future Directions Proposed by Authors

- Study populations unexposed to abstract data representations to test learned versus natural‑world origins of biases.
- Investigate experts who use light‑more encodings to see if domain expertise alters inferred mappings.
- Validate the Opacity Variation Index against perceived opacity variation.
- Examine how spatial configurations like concentric ‘hot spot’ layouts affect inferred mappings.
- Test whether strong color‑concept associations can override dark‑is‑more and opaque‑is‑more biases.



### Citations Referenced

- **Cuff (9)** — 
- **McGranaghan (22)** — 
- **Roth et al. (34)** — 
- **5 ()** — 
- **2 ()** — 
- **16 ()** — 
- **10 ()** — 
- **31 ()** — 
- **26 ()** — 
- **36 ()** — 
- **8 ()** — 
- **18 ()** — 
- **38 ()** — 
- **41 ()** — 
- **20 ()** — 
- **35 ()** — 
- **37 ()** —

<a name="critique"></a>
## Critique

*Paper: schloss-et-al-2019-mapping-color-to-meaning-in-colormap-data-visualizations*

### Overall Assessment

The paper suffers from several moderate‑severity methodological and analytical shortcomings that undermine its scholarly rigor. Key theoretical constructs (e.g., opacity variation) are insufficiently operationalized, and the primary outcome measures are ambiguous, while the statistical reporting is incomplete and occasionally inconsistent with the experimental design. Moreover, the evidentiary support for the central dark‑is‑more/opaque‑is‑more claims is weak, with contradictory results downplayed and alternative explanations not empirically ruled out. These high‑severity concerns collectively limit the paper’s credibility as a robust contribution to the literature.



### 1. Design–Theory Alignment

- **The reaction‑time outcome is used as a proxy for participants’ inferred color‑quantity mappings, but RT conflates multiple processes (e.g., perceptual difficulty, motor speed, decision confidence) and does not directly measure the theoretical bias.**
  - Severity: **moderate**
  - Justification: The theoretical claim concerns participants’ internal mapping of visual features to quantities (a cognitive bias). Measuring this bias via RT assumes that faster responses directly reflect a stronger bias, which may not hold if other factors (e.g., stimulus salience, motor preparation) influence speed. Without a more direct measure (e.g., explicit mapping judgments), the design‑theory alignment is only indirect, limiting confidence in the claimed bias effects.
  - Evidence:
    - `methods`/`exp_1` — field `outcome_measures`: reaction time operationalized as time from stimulus onset to key press
    - `results_and_discussion`/`exp_1` — field `key_findings`: RTs were faster for dark‑more encoding than light‑more encoding and varied with background and color scale
    - `introduction` — field `constructs_of_interest`: outcome defined as "inferred color‑quantity mapping" inferred from response‑time performance

- **The opacity‑variation manipulation is operationalized through an “Opacity Variation Index” that is not fully described, making it unclear whether the stimulus manipulation truly captures the theoretical construct of apparent opacity variation.**
  - Severity: **moderate**
  - Justification: The theory predicts that apparent opacity variation modulates the bias. If the index used to capture this variation is ambiguous or poorly validated, the manipulation may not align with the construct, jeopardizing the ability to test the hypothesized mechanism.
  - Evidence:
    - `results_and_discussion`/`exp_1` — field `key_findings`: RT differences correlated with Opacity Variation Index (correlations reported but calculation not explained)
    - `methods`/`exp_1` — field `materials`: description of colormap generation does not specify how opacity variation was quantified
    - `introduction` — field `mechanistic_claims`: background only matters if the colormap appears to vary in opacity

- **The predictor variable “background color” is confounded with several other stimulus dimensions (e.g., legend text position, left/right balance, and encoded lightness mapping) that also vary within the same trial, making it difficult to isolate the pure effect of background on inferred mappings.**
  - Severity: **minor**
  - Justification: Because multiple factors are manipulated simultaneously, any observed background effect could be partially driven by interactions with legend positioning or spatial balance, reducing the clarity of the test of the theoretical claim that background alone modulates bias.
  - Evidence:
    - `methods`/`exp_1` — field `design`: 5 (color scale) x 2 (background) x 2 (left/right balance) x 2 (encoded lightness mapping) x 2 (legend text position) within‑subjects design
    - `results_and_discussion`/`exp_1` — field `key_findings`: three‑way interaction between encoded lightness mapping, background, and color scale


### 2. Evidence–Theory Alignment

- **The authors claim strong support for a dark‑is‑more bias, yet key results show null or opposite effects that are downplayed, suggesting an overreach of the theoretical claim.**
  - Severity: **moderate**
  - Justification: While the paper’s central theory posits a dominant dark‑is‑more bias when opacity variation is low, the empirical data include notable exceptions that are treated as anomalies rather than evidence against the claim. By not fully addressing these contradictory results, the authors overstate the alignment between their findings and the theoretical framework, which may mislead readers about the robustness of the dark‑is‑more bias.
  - Evidence:
    - `results_and_discussion`/`exp_1` — field `anomalous_or_unexpected_results`: The Gray color scale was the only condition where RTs were not faster for dark‑more encodings on the black background, contradicting the predicted dominance of the dark‑is‑more bias.
    - `results_and_discussion`/`exp_2` — field `anomalous_or_unexpected_results`: No dark‑is‑more bias was observed for the blue‑white color scale on the black background, despite the authors’ expectation that the bias should persist when opacity does not vary.
    - `general_discussion` — field `results_stated_to_support_theory`: The discussion emphasizes that “inferred mappings were dominated by a dark‑is‑more bias” without adequately integrating the contradictory Gray and blue‑white findings.


### 3. Internal Consistency

- **The paper’s introduction posits that opacity variation should modulate inferred mappings, yet Experiment 1 does not manipulate or measure apparent opacity variation despite being presented as the primary test of the hypothesized effects.**
  - Severity: **moderate**
  - Justification: The central theoretical claim about opacity‑dependent bias shift is introduced at the paper level, but Experiment 1’s design lacks any explicit opacity‑variation manipulation, creating a gap between the hypothesis and the empirical test. This reduces the coherence of the argument that the first experiment directly addresses the opacity hypothesis.
  - Evidence:
    - `introduction` — field `specific_hypotheses`: dark‑is‑more dominance without opacity variation; opaque‑is‑more bias with opacity variation
    - `cross_section`/`exp_1` — field `rationale_for_this_experiment`: evaluate how background color influences inferred mappings when colormaps are constructed using standard visualization color scales
    - `methods`/`exp_1` — field `materials`: standard visualization color scales; no explicit manipulation of opacity variation

- **Experiment 2’s introduction states a specific prediction about an opaque‑is‑more bias affecting response times, yet the methods section does not specify the primary outcome variable, leaving the link between the predicted effect and the measured data ambiguous.**
  - Severity: **minor**
  - Justification: The experiment claims to test a precise RT‑based prediction, but the methods omit a clear definition of the dependent variable, making it unclear whether the analysis directly addresses the stated hypothesis.
  - Evidence:
    - `cross_section`/`exp_2` — field `specific_predictions`: opaque‑is‑more bias effect on RTs: faster RTs for dark‑more encoding on white backgrounds and faster RTs for light‑more encoding on black backgrounds
    - `methods`/`exp_2` — field `outcome_measures`: [] (outcome variable not specified)

- **The general discussion integrates findings from both experiments to support the opaque‑is‑more bias, yet the paper never explicitly links Experiment 1’s results to opacity variation, creating an internal inconsistency between the discussion’s claim and the presented evidence.**
  - Severity: **moderate**
  - Justification: The discussion treats Experiment 1 as providing evidence for opacity‑dependent effects, yet Experiment 1 lacked a systematic opacity manipulation, leading to a mismatch between the theoretical narrative and the empirical basis.
  - Evidence:
    - `general_discussion` — field `cross_experiment_integration`: experiment 2 supports value‑by‑alpha maps; experiment 1 explains prior reduced dark‑is‑more effect
    - `results_and_discussion`/`exp_1` — field `authors_interpretations`: participants showed a dark‑is‑more bias; opacity variation mentioned as evidence but not directly manipulated


### 4. Alternative Accounts

- **The paper dismisses the legend‑driven mapping hypothesis without providing empirical evidence that participants actually ignored the legend information.**
  - Severity: **moderate**
  - Justification: Although the authors acknowledge a legend‑driven mapping account in the introduction, they do not provide any analysis to show that participants did not rely on the legend. Without such evidence, the dismissal of this alternative remains speculative and weakens the claim that inferred mappings are driven solely by perceptual biases.
  - Evidence:
    - `introduction` — field `alternative_theories`: legend‑driven mapping hypothesis is listed as an alternative but not empirically evaluated
    - `methods`/`exp_1` — field `procedure`: participants were required to read the legend on every trial, yet no manipulation or measurement of legend reliance is reported
    - `results_and_discussion`/`exp_1` — field `authors_interpretations`: authors treat the legend as merely a cue and do not test whether it overrides perceptual biases

- **The design may not adequately distinguish the focal dark‑is‑more/opaque‑is‑more account from a pure contrast‑is‑more bias, yet the authors claim to have challenged the latter.**
  - Severity: **moderate**
  - Justification: Because opacity variation and contrast co‑vary across the color scales used, the experiment cannot cleanly separate a contrast‑is‑more effect from the proposed opaque‑is‑more effect. Claiming to have refuted the pure contrast account therefore overstates what the data can support.
  - Evidence:
    - `general_discussion` — field `description`: contrast‑is‑more bias is said to be challenged, but no direct contrast‑only condition (e.g., varying contrast while holding opacity constant) is presented
    - `results_and_discussion`/`exp_1` — field `key_findings`: interactions involve background, encoded mapping, and color scale, but opacity variation is confounded with contrast changes across scales
    - `general_discussion` — field `results_stated_to_challenge_theory`: authors state the result challenges pure contrast‑is‑more bias without showing a condition that isolates contrast effects


### 5. Statistical Completeness

- **Experiment 1 does not report the main effects of the two additional within‑subject factors (legend text position and left/right balance) that were part of the 5 × 2 × 2 × 2 × 2 design.**
  - Severity: **moderate**
  - Justification: The analysis plan should include all factors from the design. Omitting the main effects (and any interactions) of legend text position and left/right balance leaves the statistical reporting incomplete for a fully factorial ANOVA.
  - Evidence:
    - `methods`/`exp_1` — field `predictors`: predictors list includes legend text position and left/right balance as factors
    - `results_and_discussion`/`exp_1` — field `key_findings`: reported effects only involve encoded lightness mapping, background, color scale, and their interactions; no mention of legend text position or left/right balance

- **Experiment 1 reports a three‑way interaction (encoded lightness × background × color scale) but provides simple‑effects follow‑up only for a subset of color scales (Autumn, Hot, Blue, Gray) and does not report simple effects for all combinations of background and color scale within that interaction.**
  - Severity: **moderate**
  - Justification: When a higher‑order interaction is significant, standard practice is to decompose it by reporting simple effects for all constituent cells. The partial follow‑up leaves the interaction only partially explored.
  - Evidence:
    - `results_and_discussion`/`exp_1` — field `key_findings`: three‑way interaction reported (F(3,87)=13.94) and simple‑effects described for Autumn, Hot, Blue, and Gray, but no simple‑effects are given for the interaction of encoded lightness with background for the Autumn scale, nor for all background‑by‑scale cells

- **Experiment 1’s color‑scale factor originally had five levels (MATLAB Autumn, Hot, Gray, ColorBrewer Blue, MATLAB Jet) but the ANOVA results treat it as having four levels (F(3,87) reports), and the Jet scale is never mentioned in the results.**
  - Severity: **moderate**
  - Justification: The discrepancy suggests that the analysis either omitted one level or collapsed it without explanation, resulting in incomplete reporting of the factorial design.
  - Evidence:
    - `methods`/`exp_1` — field `predictors`: color scale factor listed with five levels
    - `results_and_discussion`/`exp_1` — field `key_findings`: main effect of color scale reported with df=3 (implying four levels) and subsequent pairwise comparisons only involve Autumn, Hot, Blue, and Gray

- **Experiment 2 does not report the main effects or interactions involving the two additional factors (legend text position and left/right balance) that were part of its 5 × 3 × 2 × 2 × 2 design.**
  - Severity: **moderate**
  - Justification: Full factorial reporting requires presenting results for all factors. Their omission leaves the statistical analysis incomplete.
  - Evidence:
    - `methods`/`exp_2` — field `predictors`: predictors list includes legend text position and left/right balance
    - `results_and_discussion`/`exp_2` — field `key_findings`: ANOVA results only mention main effect of lightness mapping, its interaction with background/color‑scale relation, and a non‑significant three‑way interaction; no effects for legend text position or left/right balance are reported

- **Experiment 2 reports a significant interaction between lightness mapping and background/color‑scale relation but does not provide simple‑effects or post‑hoc comparisons for each of the three background‑by‑color‑scale conditions (opacity‑varying light, opacity‑varying dark, no opacity variation).**
  - Severity: **moderate**
  - Justification: A significant interaction should be followed by detailed simple‑effects analyses for each level of the interacting factor to fully characterize the pattern of results.
  - Evidence:
    - `results_and_discussion`/`exp_2` — field `key_findings`: interaction reported (F(2,58)=50.47) and simple effects are described for each condition, but the reporting does not include effect sizes or confidence intervals for all three conditions, nor does it test the interaction contrast directly


### 6. Methodological Concerns

- **No a priori power analysis is reported for either experiment, leaving the adequacy of sample size unclear.**
  - Severity: **moderate**
  - Justification: Both experiments list 30 participants but explicitly note that power analysis was not reported. Without justification of sample size, it is uncertain whether the studies were sufficiently powered to detect the hypothesized effects, especially given the large number of within‑subject conditions.
  - Evidence:
    - `methods`/`exp_1` — field `power_analysis`: null
    - `methods`/`exp_2` — field `power_analysis`: null

- **Preregistration status is not reported, raising concerns about potential undisclosed analytic flexibility.**
  - Severity: **moderate**
  - Justification: The methods sections for both experiments state "preregistration_status": "not reported", which suggests that the studies were not preregistered or that this information is omitted, limiting transparency about planned versus post‑hoc analyses.
  - Evidence:
    - `methods`/`exp_1` — field `preregistration_status`: not reported
    - `methods`/`exp_2` — field `preregistration_status`: not reported

- **Counterbalancing procedures are insufficiently described, particularly for Experiment 2 where the scheme is omitted entirely.**
  - Severity: **minor**
  - Justification: While Experiment 1 mentions a blocked randomized design, it lacks detail on how condition order was balanced across participants. Experiment 2 provides no information on counterbalancing, making it unclear whether order effects could have influenced the results.
  - Evidence:
    - `methods`/`exp_1` — field `counterbalancing`: blocked randomized design; all 80 conditions displayed once in random order within each block
    - `methods`/`exp_2` — field `counterbalancing`: not reported

- **Outcome variable(s) are not explicitly defined for Experiment 2, hindering replication and interpretation.**
  - Severity: **moderate**
  - Justification: The methods for Experiment 2 list an empty outcome_measures array, yet the results focus on reaction times. This omission reduces methodological transparency and may affect how the analysis was planned.
  - Evidence:
    - `methods`/`exp_2` — field `outcome_measures`: []
    - `results_and_discussion`/`exp_2` — field `key_findings`: All findings refer to RTs, but the methods never state that reaction time is the primary dependent variable.

- **Exclusion criteria are incompletely specified beyond a few explicit cases, leaving ambiguity about data cleaning decisions.**
  - Severity: **minor**
  - Justification: Both experiments mention specific exclusions but do not provide a comprehensive set of criteria (e.g., reaction‑time outliers, failed attention checks). This lack of detail hampers reproducibility and may introduce bias.
  - Evidence:
    - `methods`/`exp_1` — field `exclusions`: experimenter error in giving the instructions (3 participants excluded)
    - `methods`/`exp_2` — field `exclusions`: participants with overall accuracy ≤ 90% (6 excluded)
    - `methods`/`exp_1` — field `missing_or_unclear`: Exclusion criteria beyond the three participants excluded for instruction error not described
    - `methods`/`exp_2` — field `missing_or_unclear`: no further exclusion criteria reported


### 7. Statistical Robustness

- **The paper reports numerous significant effects without providing confidence intervals for the estimated effects, limiting assessment of the precision of the findings.**
  - Severity: **minor**
  - Justification: Confidence intervals are essential for evaluating the reliability and practical significance of reported effects, especially in within‑subjects designs with many comparisons. Their absence hampers readers’ ability to gauge the robustness of the statistical conclusions.
  - Evidence:
    - `results_and_discussion`/`exp_1` — field `key_findings`: All reported ANOVA results include F, p, and ηp² values but no confidence intervals for means or effect sizes.
    - `results_and_discussion`/`exp_2` — field `key_findings`: Similarly, repeated‑measures ANOVA and simple‑effect tests are presented with F, p, and ηp² but without confidence intervals.

- **A marginal effect (p = .079) is described as a "trend" and discussed as potentially meaningful, which may overstate its evidential weight.**
  - Severity: **moderate**
  - Justification: Labeling a non‑significant p‑value as a trend can mislead readers into interpreting the effect as supportive evidence. Given the p‑value exceeds the conventional .05 threshold, the claim should be qualified more cautiously.
  - Evidence:
    - `results_and_discussion`/`exp_1` — field `key_findings`: For the Gray color scale on the black background, the interaction is reported with "p = .079" and described as "a trend toward faster RTs for light-more encoding on the black background".
