## Participants

We recruited subjects via Amazon’s Mechanical Turk (MTurk) crowdsourcing platform. Prior research has established the validity of crowdsourcing experiments for controlled quantitative modeling in color perception [34, 40]. While we sacrificed control over monitor display and situational lightning conditions, we gained samples from a wider variety of display conditions in the real-world web user population. In addition, the variance introduced by viewing conditions is partly accounted for by per-subject random terms in our statistical models. Each experiment run was implemented as a single Human Intelligent Task (HIT) to ensure a within-subjects design. We restricted the participants to be within the United States and to have an acceptance rate over 95%.

## Procedure

We first screened the participants for color vision deficiencies using four Ishihara plates. As factors including uncalibrated displays and image compression can make Ishihara plates unreliable, we also stated in the consent page that participants must have normal color vision. The participants then read a tutorial page with a sample question, which encouraged them to use the color legend, explaining that the correct answer should be deduced from value differences in the legend. Prior to the experiment, we administrated a practice session consisting of 5 trials from an irrelevant colormap to reduce learning effects.

![](images/6bd5b9f2692f18005caaf5f7f64a6a93f526cf32a9b779fd2fa75aa5fd29a9fe.jpg)  
(a) Assorted Colormaps

![](images/c1690c0b27b1543224fc008dc0aeabd2a4ea6f733e1af8339e1fabd60d8b8277.jpg)  
(b) Single-Hue Colormaps

![](images/b55169eeddab02cdad4ab9d58a6fb39ee16d243641a44239229f10eb174afe42.jpg)  
(c) Multi-Hue Colormaps  
Figure 3: Log response time by colormap for each study. Plots depict bootstrapped means, with 50% (thick) and 95% (thin) CIs. (a) Assorted colormaps. The single-hue colormap blues is the fastest, followed by viridis. The rainbow colormap jet is the slowest. (b) Single-hue colormaps. Subjects spent almost identical time on average on each colormap. (c) Multi hue colormaps. UCS multi-hue colormaps are comparable in speed. Viridis is slightly faster, but not significantly so.

Participants completed blocks of trials for each colormap, with an option to take breaks between sessions to mitigate fatigue. We asked subjects to respond as quickly and accurately as possible, prioritizing accuracy. We counterbalanced the colormap order using either a Balanced Latin Square or a full permutation of all possible orders, depending on the total number of colormaps in each study. We randomized the question order for each colormap. An engagement check question appeared randomly per colormap block to ensure attentive participation.

In each trial, we simultaneously presented the three color stimuli arranged in a triad, with a legend that included ticks at each 10 unit interval (Figure 2). Participants responded by clicking on the choice square and clicking the “Next” button, or by pressing the “a” or “b” key followed by “enter”.

## Data Analysis

Our primary dependent variables are log-transformed response time (RT) and an error label, indicating whether a subject answered the question correctly. Observing that RT follows a log-normal distribution, we performed log transformation. The error response uses a binary coding of 1:error, 0:correct. To visualize effect sizes, we calculate bootstrapped confidence intervals (created by sampling entire subjects, not individual responses, with replacement) and plot both 50% and 95% CIs.

Previous quantitative modeling on color perception has fit linear models to the mean proportion of response, obtained by averaging individual binary outcomes per cell [39, 40]. This approach discards a large portion of the individual variance. As a result, the fitted model describes the mean performance from a sample group of the population, but not the performance of any individual.

![](images/2ae541f090bd68a721914a6fc117f7ce0be269d6354bd872b4a0a09bc0685eca.jpg)  
(a) Assorted Colormaps

![](images/bdd2d417a215b4536905ca4e3a2280f8436eb15b025abf948d2166d0b04d31e3.jpg)  
(b) Single-Hue Colormaps

![](images/5d15d45e4c1e3368e0a1c25081c725df2784ec1579cd7f028b6feb834791a9ad.jpg)  
(c) Multi-Hue Colormaps  
Figure 4: Error rate by colormap for each study. Plots depict bootstrapped means, with 50% (thick) and 95% (thin) CIs. (a) Assorted colormaps. Viridis excels in accuracy while jet is the most error-prone. (b) Single-hue colormaps. Though slightly faster, blues and greens have overlapping confidence intervals with the slower colormaps, oranges and greys. (c) Multi-hue colormaps. Multi-hue colormaps have comparable accuracy within group. The per-colormap average error rate of magma is higher as it contains degenerate cases.

In this paper, we instead fit models to individual observations, using linear mixed-effects models for RT and logistic mixedeffects models for error (using the lme4 package in R [2]). Mixed-effects models can incorporate random effect terms to account for variation arising from subjects as well as other sources. In our models we include fixed effect terms for colormap, span, and their interaction. Following Barr et al. [1], we also include maximal random effects structures with persubject terms for random intercept (capturing overall bias) and random slopes for each fixed effect (capturing varied sensitivities to experiment conditions). As we later show, specific colors may exhibit outlying performance relative to a colormap as a whole. In response, we include random intercepts for each unique reference color (i.e., colormap / reference value pair) to improve generalization of fixed effect estimates.

## EXPERIMENTAL RESULTS

We now present the results from our three experimental runs. We first share the results from each colormap group, and then investigate special cases with surprisingly low or high error rates. Figures 3 and 4 show global time and error estimates per colormap. Figures 5, 6, 7, and 8 provide more detailed plots across span and reference conditions.

Across colormap groups we conducted a diagnostic analysis before examining time and error separately. In all cases we note a similar, positive correlation between response time and error: on average, subjects spend more time on the more difficult cases. This result suggests that the performance measures are not simply the result of varied speed/accuracy trade-offs.

## Assorted Colormaps

A total of 56 subjects (19 female, 36 male, 1 other, $\mu _ { a g e } = 3 5 . 3$ years, $\sigma _ { a g e } = 8 . 9$ years) participated in the assorted colormap study. Subjects completed the study in 15 minutes on average and were compensated \$2.00 USD.

Time: Blues & Viridis are Faster than BlueOrange & Jet Likelihood ratio tests of linear mixed-effects models for log response time found significant main effects for colormap $( \chi ^ { 2 } ( 9 ) = 6 0 . 5 , p < 0 . 0 \bar { 0 } 1 )$ , span $( \chi ^ { 2 } ( 8 ) = 6 0 . 0 , p < 0 . 0 0 \dot { 1 } )$ and their interaction $( \chi ^ { 2 } ( 6 ) = 2 6 . 3 , p < 0 . 0 0 1 )$ . To compare response times across colormaps, we applied post-hoc tests with Holm’s sequential Bonferroni correction. We find that both blues and viridis are significantly faster than blueorange $( p < 0 . 0 1$ , both cases) and jet $( p < 0 . 0 0 1$ , both cases). The difference in means between blues and viridis is not significant, nor is the difference between blueorange and jet.

With respect to span, subjects performed significantly slower when the span was 60 compared to a span of 30 $( p < 0 . 0 1 )$ ) or 15 $( p < 0 . 0 5 )$ . The significant interaction between colormap and span stems primarily from blues, which was relatively slow for small spans. As we will discuss shortly, this decrease in performance correlates with more pronounced errors.

Subjects made faster judgments with the viridis and blues colormaps and spent more time determining distances with blueorange and jet, presumably because the distances are not as apparent. This discrepancy may result from increased effort discerning perceptual similarities and/or consulting color legends. Across all colormaps, more time was needed when colors were further apart in the color scale.

## Error: Viridis Excels; Blues Degrades for Low Spans

Tests of logistic mixed-effects models for error again found significant effects of colormap $( \chi ^ { 2 } ( 9 ) = 4 6 . 0 , p \stackrel { . } { < } 0 . 0 0 1 )$ , span $( \chi ^ { 2 } ( 8 ) = 4 2 . 9 , p < 0 . 0 0 1 )$ , and their interaction $( \chi ^ { 2 } ( 6 ) = 2 8 . 6 $ $p < 0 . 0 0 1 )$ . Post-hoc tests revealed that viridis is less errorprone than blues and jet (both $p < 0 . 0 0 1 )$ . Across colormaps participants made fewer mistakes on average in the smallest span compared to other levels (both $p < 0 . 0 0 1 $ ). The interaction effect again stems from the differential characteristics of blues: when the span was small, error increased. An example of such triplets $\mathrm { i s } \mathbf { \bar { \Pi } }$

In a follow-up analysis where for all colormaps we dropped responses for span 15, a significant effect of colormap on error rate $( p < 0 . 0 0 1 )$ ) remains, but without a significant interaction. In this case we did not observe a significant difference between viridis and blues in error rate, but blues outperforms jet and blueorange $( p < 0 . 0 5 )$ .

![](images/ffbc95013446bbbb1cedb6c279a1b7a849db50ad9fa8c368746fe650dd0fdbc7.jpg)

![](images/98b0697df942dc1d32a77fc7ee18703e6af26d9a2d1efd5b1f9019042bd9dd46.jpg)

![](images/7f017c6ef6bf62885b3bfd4739f3da3b21a282a5bf8aed648a9cab20dac0231f.jpg)

![](images/ce264314bf72851b8fa043ce46242d67df20b4ed65a118727b4d0379d283263b.jpg)  
Figure 5: Log response times by span and reference for assorted colormaps. Points indicate bootstrapped means, along with 50% (thick) and 95% (thin) CIs. Each sub-plot includes the mean value for each span level (dotted grey line). Across colormaps, response times increase with larger spans. Jet exhibits the longest response times.

![](images/5e71d049f25f76bd72c2979606b15c231aebbfc4f4b4c24a326274d5c45a1b82.jpg)

![](images/4301dd3c3602f69c17c01c10340fe8ecd95355758d555bd187a36ea0f619d44a.jpg)

![](images/3412064bf00e0c330b01d8925d627fa17f3bcfd88a933593bf08c0ac859f496f.jpg)

![](images/91f63bb462da473c5b7c7aaab10442820ae4828974991266e3defa20c8d8a27d.jpg)  
Figure 6: Error rate by span and reference for assorted colormaps. Points indicate bootstrapped means, along with 50% (thick) and 95% (thin) CIs. Each sub-plot includes the mean value for each span level (dotted grey line). Viridis exhibits consistently low error across the board. The accuracy of blues matches that of viridis at larger spans, but drops notably for the smallest span. The blueorange diverging scheme exhibits errors when comparison is made across the central blue-orange hue boundary.

## Summary

In this study, viridis demonstrated both superior speed and accuracy. Blues performed comparably well at spans 30 and 60: it was fast and accurate so as long as there was sufficient spacing between adjacent colors. However, once the colors were too close in the color scale, the accuracy of blues dropped con siderably, together with a mild increase in response time. The diverging colormap blueorange and the rainbow colormap jet were both slower and more error-prone. We examine special cases affecting these latter two colormaps later in the paper.

Comparing with the subsequent studies, we note similar error results for replicated colormaps, but systematically lower response times in the assorted colormaps group (Figure 3). We attribute this disparity in part to individual differences. For example, 64.3% of participants were male in the assorted group, while single-hue and multi-hue groups were 33.9% and 42.6% male respectively. In a linear mixed-effects model of RT with gender as the fixed effect, fit to data from all three experiments, the male group was significantly faster $( p < 0 . 0 1 )$ . We found no significant effect of gender in a similar model for error.

## Single-Hue Colormaps

56 subjects (36 female, 19 male, 1 other, $\mu _ { a g e } = 3 7 . 2 , \sigma _ { a g e } =$   
11.1) were assigned single-hue colormaps. Subjects averaged   
15 minute sessions and were compensated \$1.60 USD.

![](images/953706a58b44cb8da260bfa2614ddb59ccf469be145e73fe3bc0924685b2e22b.jpg)

![](images/7f7fe541fd3c76b5bbd8e4269eabfeceae93d8ff4739e5417c06efb672cece51.jpg)

![](images/96bf7fdecf55cee8ed13e3499b28bd48d3a91b6f6a871909c0a0b8974428f97f.jpg)

![](images/e7bc6fa0d4003541021a8b2f1daae8c7cd5d1a26bfe290234009ff6b0853f531.jpg)  
Figure 7: Error rate by span and reference for single-hue colormaps. Points indicate bootstrapped means, along with 50% (thick) and 95% (thin) CIs. Each sub-plot includes the mean value for each span level (dotted grey line). All single-hue colormaps similarly suffer from resolution issues when the span is small. Greys degenerates in low luminance regions.

![](images/933c6da4564295faf782b4f3ff570348fc3c25a763b41ef95fa934a66d6c374f.jpg)

![](images/a1e251253894f2d49f381aa1de3c1ce948f541bd96c856310f42917670586021.jpg)

![](images/96dbc51271dfac3d884f42ce6486c277079b8454b60d37d68ae2644b971ab42f.jpg)  
Figure 8: Error rate by span and reference for multi-hue UCS colormaps. Points indicate bootstrapped means, with 50% (thick) and 95% (thin) CIs. Each sub-plot includes the mean value for each span level (dotted grey line). We observe similar dynamics across colormaps. Performance degrades in the dark region of magma, and to a lesser extent of plasma.

## Time: No Differences in Single-Hue Responses

In a linear mixed-effects model of RT, we found a significant effect of span $( \chi ^ { 2 } ( 8 ) = 3 9 . 9 , \ p < 0 . 0 0 1 )$ , but not for colormap or their interaction. This result is consistent with the per-colormap means plotted in Figure 3: participants have similar response times $\dot { ( } \sim 1 0 ^ { 3 . 3 9 } = \stackrel { \smile } { 2 } , 4 5 4$ milliseconds) for each colormap in the single-hue group.

## Error: Single-Hue Colormaps Suffer from Low Resolution

Tests with a logistic mixed-effects model of error found a significant effect of span $( \chi ^ { 2 } ( 8 ) = 8 6 . 0 , p < 0 . 0 0 1 )$ , but no significant colormap or interaction effect. This result is consistent with Figure 4: despite lower means, 95% CIs for blues and greens overlap with those for oranges and greys. Looking across studies, we see very similar error profiles for blues in Figures 6 and 7, indicating successful replication.

Post-hoc comparisons confirmed that error rates for span 15 are significantly higher than span 30 $( p < 0 . 0 5 )$ or span 60 $( p < 0 . 0 5 )$ . This result corroborates the increased errors for blues in low-span cases in the prior study, and extends it to a larger family of single-hue colormaps. These colormaps suffer from poor resolution for nearer value comparisons.

To further test this claim, we calculated the LAB distances between the reference stimulus and the two choices respectively, and subtracted them to obtain a difference measure in units of ∆E. We found that in low-span conditions where accuracy plummets, the ∆E difference is around 5, close to the justnoticeable difference (JND) found in practical situations [39, 40]. Though the ∆E between each stimulus is large enough for the colors to be distinguishable, the difference in ∆E between pairs is hard to discriminate, leading to increased error.

## Multi-Hue UCS Colormaps

54 subjects (31 female, 23 male, $\mu _ { a g e } = 3 6 . 7 , \sigma _ { a g e } = 1 0 . 1 )$ participated in the multi-hue colormap study. We discarded

data from 1 subject (2%) due to missing responses. Subjects averaged 12 minute sessions and paid \$1.20 USD.

## Time & Error: Multi-Hue Colormaps are Comparable

Analysis of the multi-hue UCS colormaps detected no significant differences between colormaps in terms of either response time or error rate. Figure 3 shows that the mean response times align around 2.82 seconds $( 1 0 ^ { 3 . 4 5 }$ milliseconds). Similarly, the mean error rates of viridis and plasma are slightly lower than that of magma, but exhibit overlapping 95% CIs (Figure 4). The more detailed plots in Figure 8 reveal spikes in error rate for magma, and to a lesser extent plasma, around low reference values. We examine this issue further in the next section.

Multi-Hue UCS Colormaps have Lowest Error Across Studies Comparing across studies, the error profiles for viridis in Figures 6 and 8 are quite similar, indicating successful replication. We see that across studies the UCS colormaps exhibit the lowest error rates, though with slightly longer response times.

## Analysis of Special Cases

The above section analyzes colormaps in terms of their mean performance, with models that include random effects to account for some of the larger swings among specific reference points. Here we perform a complementary analysis, investigating the specific conditions in which error rates are surprisingly high or low. We take a closer look at (1) error increases in low luminance conditions (greys, magma, plasma), (2) the performance of the diverging blueorange colormap, and (3) a special case where jet – the colormap with worst performance overall – exhibits extremely low error.

## Performance Degrades in Low Luminance Regions

An obvious abnormality across studies and colormaps is a dramatic increase of error rates in the black regions, particularly greys, magma, and, to a lesser degree, plasma (Figures 7 and 8). For example, the magma triplets (0, 10, 15) and (5, 10, 20) exhibit high error. The affected conditions all involve small values in the luminance channel; the low luminance level appears to afford much worse color discrimination than that predicted by either the LAB or UCS perceptual models. This observation is likely specific to our choice of a white background, with the high contrast impeding the discrimination of dark shades. We hypothesize that an analogous shortcoming will occur for high luminance shades set against a dark background.

## BlueOrange Suffers when Values Straddle the Mid-Point

A closer look at blueorange suggests a primary source of errors (Figure 6). When all three triplet colors lie on a singlehue half of blueorange, the performance closely matches that of the corresponding single-hue colormap. For example, the first three points in the small span plot of blueorange average about 10%, similar to the mean error rates of blues for the medium span (Figure 6, 7). Note that we double the span to compare to single-hue colormaps, as each hue takes up one-half of the range of the diverging colormap. As indicated by the high error rates in the middle of blueorange, subjects were prone to mistakes when making comparisons across the blue-orange boundary. A representative triplet is (50, 60, 80), where the lower, achromatic option is closer than the similarly-hued, but much more saturated, option. This result suggests that diverging colormaps may be less accurate in situations involving comparisons with the mid-point, perhaps due to erroneous grouping of chromatic colors versus a nearer achromatic color.

## Where the Rainbow Shines: Color Name Association

Though the majority of reference stimuli in jet lead to higher error than other colormaps, reference value 50 performs remarkably well at span 15 (Figure 6). In the small span condition this reference point has a mean error rate as low as 3.5%, which is among the lowest in all observations! The corresponding color triplets are (40, 50, 55) and (45, 50, 60). These triplets lie in an isoluminant region of jet: there are no luminance cues that might suggest ordering. Instead, these triplets happen to straddle color name boundaries that align with the underlying value differences. Color name distances [21] from the reference average 0.23 and 0.94 for the nearer and further values, respectively. The first triplet has modal names of cyan versus two greens, while the second triplet has two greens versus yellow. This result suggests that categorical effects, or banding by name, can contribute to improved discrimination if applied in the right direction and, conversely, may hamper perception if dischordant with the true value difference.

## COLOR MODEL ANALYSIS

In addition to empirical characterization of user performance, we would like to have a theoretical model. For example, given a previously untested colormap, might we predict its relative performance? If so, we could use the model to automatically optimize colormap designs. To assess this question we construct a series of models that attempt to generalize beyond the specific colormaps using a set of three color distance models:

• LAB: The CIELAB color space [24].

• UCS: The CAM02-UCS uniform color space model [28].

• Name: The color name model of Heer & Stone [21].

The first two color models (LAB and UCS) provide perceptual color spaces that approximately model perceptually uniform color distances. We include both for comparison. For LAB, we use Euclidean distance (∆E) to measure color distance. The third model (Name) is a model of categorical effects that measures color difference by comparing the distributions of observed color terms (e.g., orange, blue, fuchsia) that people use to label color swatches. The Name model is included to capture categorical effects of color naming that may not be reflected by the perceptual models. Following prior work [21], we use a cosine distance measure between color term vectors.

To apply these measures to a triplet comparison task, we first compute the color model differences between the reference stimulus and the two response stimuli. We then calculate the difference of the predicted color model distances; i.e., we simply subtract the distance value for the correct answer from the distance value for the incorrect answer. A negative difference indicates that the correct answer (the more similar data value) is further away according to the distance measure. A positive difference indicates a larger distance for the incorrect answer (the more dissimilar data value).

<table><tr><td>Model</td><td>df</td><td>AIC</td><td>BIC</td><td>logLik</td><td>deviance</td></tr><tr><td>LAB</td><td>24</td><td>21668</td><td>21863</td><td>-10810</td><td>21619</td></tr><tr><td>UCS</td><td>24</td><td>21665</td><td>21860</td><td>-10808</td><td>21617</td></tr><tr><td>Name</td><td>24</td><td>21585</td><td>21781</td><td>-10769</td><td>21537</td></tr><tr><td>UCS + Name</td><td>63</td><td>21308</td><td>21821</td><td>-10591</td><td>21182</td></tr><tr><td>UCS * Name</td><td>288</td><td>21377</td><td>23723</td><td>-10401</td><td>20801</td></tr></table>

Table 1: Diagnostics for error models based on color model distances. Columns indicate degrees of freedom (df), AIC and BIC model selection scores, log-likelihood (logLik) and deviance. An additive model with UCS and color name difference terms achieves the best balance of fit and parsimony according to AIC and BIC scores (lower is better).

## Error Analysis

To predict error rates, we fit a logistic regression model. We use mixed-effects models with random effect terms for both subject (to account for variance due to individual differences) and colormap (each trial includes presentation of a color legend, and we account for this in order to estimate more generalizable fixed effects). We use maximal random effects structures [1], with intercepts for each random effect and corresponding random slope terms for each fixed effect.

We first assessed which form the predictor should take. We examined both direct use of color model difference estimates (a continuous, linear predictor) and binned factors based on quartile boundaries (a discrete, potentially non-linear predictor). All fitted models exhibit statistically significant fixed effect estimates, via both Wald z-tests and Likelihood Ratio tests. The binned predictor leads to better models for all color difference types: with improved fit (log-likelihood and deviance) and lower model selection scores (AIC, BIC). As a result, we focus on the discrete predictors.

Next, we compare these single-effect models to assess performance differences among color difference types. Which color model most accurately predicts performance? Table 1 shows the resulting model diagnostics. We see that name difference performs the best according to all measures. The UCS model outperforms LAB, but by a miniscule margin. Overall, the differences between the three models are small.

We then fitted two-factor models that include perceptual and categorical terms. For the perceptual term we chose UCS rather than LAB for two reasons. First, UCS performs slightly better than LAB as a single predictor. Second, the color name model internally applies a fine-grained discretization of the LAB color space, and so is likely to exhibit higher correlation with LAB. We built models both with and without interaction terms. The last two rows of Table 1 show the resulting model diagnostics. Both models improve upon the single-factor models in terms of fit and AIC score. The model with interaction terms exhibits improved fit (higher log-likelihood and lower deviance), but this is unsurprising given the greater degrees of freedom. The additive model has lower AIC and BIC scores than the full model, indicating a more parsimonious model. To avoid overfitting, we stop with the additive model.

<table><tr><td>Parameter</td><td>Estimate</td><td>Std. Error</td><td>P-Value</td><td></td></tr><tr><td>Intercept</td><td>-1.0848</td><td>0.1804</td><td>&lt; 0.001</td><td>***</td></tr><tr><td>UCS_Q2</td><td>-0.4031</td><td>0.2043</td><td>0.048</td><td>*</td></tr><tr><td>UCS_Q3</td><td>-0.5298</td><td>0.1618</td><td>0.001</td><td>**</td></tr><tr><td>UCS_Q4</td><td>-0.4452</td><td>0.2482</td><td>0.073</td><td></td></tr><tr><td>Name_Q2</td><td>-0.5009</td><td>0.1641</td><td>0.002</td><td>**</td></tr><tr><td>Name_Q3</td><td>-0.6309</td><td>0.1621</td><td>&lt; 0.001</td><td>***</td></tr><tr><td>Name_Q4</td><td>-0.6207</td><td>0.1336</td><td>&lt; 0.001</td><td>***</td></tr></table>

Table 2: Fixed effect parameter estimates and p-values for a logistic regression model (UCS + Name) of judgment error. Increasing UCS and Name difference lead to lower error, but this effect attenuates in the highest quartile.

Table 2 shows the coefficients of the resulting model. The intercept term is the logit value for triplets with difference values residing in the first quartiles for both UCS and Name. As the color differences increase, we see increasingly negative coefficients, indicating lower error rates. However, for both UCS and Name this trend tapers off for the highest quartile (Q4): relative to the earlier quartile (Q3), the error slightly increases for the largest color differences. This effect may stem from issues with large distances in perceptual color spaces: perceptually uniform color spaces were constructed in accordance with empirical color discrimination judgments at a small scale (e.g., 10-20 ∆E [28]). As a result, longer scale distances in these models are known to be more inaccurate.

How well do these color models predict user performance overall? To assess this question, we can use the additive model to predict the average performance across all experimental conditions. While this is “testing on the training data” and so not a means of assessing generalization, it nevertheless serves as a useful diagnostic. Comparing the model’s predicted error rates with the observed rates via standard linear regression, we achieve of an R<sup>2</sup> value of 0.108. In other words, our fitted model only explains about 10% of the observed variance.

We can also examine model predictions for the average performance of each colormap: does our model rank the colormaps in an order similar to the observed error rates? The Spear man rank correlation between the model predictions and the observed empirical error rates (ρ = 0.45) is not high and not statistically significant. In short, the fitted model does an unsatisfactory job of predicting overall colormap performance.

## Time Analysis

To analyze timing responses, we followed a similar procedure as we did for the error analysis, but using linear mixed-effects models of the log-transformed response times rather than logistic regression. Once again, the binned variants outperform the linear predictors. For the single-factor models, UCS outperforms LAB, which outperforms Name. Comparing a full model with UCS, Name, and interaction terms to a model without an interaction term again finds that the full model exhibits worse AIC and BIC scores.

Using the additive (UCS + Name) model to predict percondition average response times in the log domain results in an $R ^ { 2 }$ value of 0.244, accounting for 24% of the observed variance. The rank correlation of observed per-colormap average responses with model predictions $( \rho = 0 . 6 7 )$ is higher than for error, but again is not statistically significant.

## Summary

Combining perceptual color models and color naming models leads to higher predictive accuracy for both time and error than either alone. This suggests that lower-level perception and language-level processes may both play a role in the interpretation of quantitative color encodings. We also observe that increasing perceptual and name differences correlate with higher judgment accuracy, but that this trend is non-linear, tapering off among the highest quartile of differences for both measures. That said, we believe the primary take-away is a need for caution, as neither the error model nor time model lead to accurate prediction of the observed experimental results (let alone for new, unseen conditions).

Improved models or measures could lead to more accurate predictions of user performance. Some issues may arise from the triplet comparison task: perceptual color models are fit to pairwise discrimination judgments, and so may be less well-suited for the comparison tasks studied here. Moreover, our measures of difference do not take into account either the relative color space locations or the magnitude of the underlying color distances, only their difference. In addition, the inclusion of color legends in each trial may affect the predictive utility of color models. If our experiments were re-run without a visible color legend – such that subjects must make similarity judgments based on perception alone – it is possible that the results might align more closely with color model predictions. We leave exploration of these possibilities to future research.

## DISCUSSION AND FUTURE WORK

In this work we evaluated nine quantitative colormaps using a relative similarity judgment task across varied spans of the data domain. We found that more recent multi-hue colormaps created using the CAM02-UCS color space – particularly viridis – perform well in terms of time and error. Single-hue colormaps perform well for larger data spans (i.e., judgments made over larger scale ranges), but exhibit issues of insufficient resolution at smaller spans. These results suggest that, by ramping in both luminance and hue, multi-hue colormaps can provide improved discrimination while preserving perception of order. We found that a diverging blueorange colormap performs similarly to the single-hue colormaps from which it is composed, but exhibits increased error for comparisons that straddle the mid-point. Finally, we confirmed that a rainbow colormap (jet) does indeed perform the worst overall in terms of both time and error, and should be jettisoned.

Our results provide actionable guidance for colormap design and selection. First, we establish benefits for judiciously designed multi-hue colormaps. In situations involving use of a continuous color scale to visualize a scalar field (e.g., in heatmaps), multi-hue colormaps may be preferable to singlehue given their improved resolution. For applications involving discrete color scales (i.e., with 5-7 colors), single-hue colormaps may still be acceptable; however, using a larger number of bins can result in color differences that fall within the low-span conditions studied here.

Second, we identify issues with low luminance regions set against a white background. Across colormaps (greys, magma, plasma), we observed much higher error rates despite similar distance estimates from perceptual color space models. We advise designers to avoid using these colormaps in situations with a high-luminance background, and warn that similar issues may arise when visualizing data using high-luminance colors against a dark background.

In a subsequent modeling exercise, we found that a combination of perceptually-uniform color models and categorical effects due to color naming can more accurately predict user performance than either alone. Larger perceptual and categorical differences correlate with improved accuracy, though with slightly diminishing effects for extreme differences. However, more work is needed to form more accurate models if we wish to advance automated colormap design and evaluation.

One limitation of the present work arises from our exchange of experimental control for ecological validity: through MTurk, we give up control of the viewing environments, the visual angle of the stimuli, along with other situational factors that confound color perception. Another limitation comes from our choice to present isolated color patches on a white background. Though white backgrounds are the most common both in print and on screen, our current setup is limited in its scope. Our experiments might be extended to other backgrounds, for example to see if analogous performance degradation occurs for light colors set in a dark context.

We chose to conduct an experiment on triplet comparison tasks in an abstracted context, configured to align with a standard observer model. However, visualizations in the wild involve a larger array of simultaneously presented colors, often involving variably sized marks across a variety of spatial configurations, and used for multiple perceptual tasks. These differences may very well affect colormap performance, for example due to simultaneous contrast. Similarly, while many of our findings likely still hold in scalar field visualizations, dedicated experiments in scalar field contexts might uncover additional effects of spatial frequency and gradients. Though our results provide actionable insights regarding the performance of colormaps in comparison tasks, future work might extend the findings to more real-world visualization examples.