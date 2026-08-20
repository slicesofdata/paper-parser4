## Method

We asked users to parameterize the display of chart gridlines drawn over a plotting area. In task L, we asked subjects, “Adjust the grid so that it is as light as possible while still being usably perceptible.” In task D, we instructed them, “Adjust the grid strength to meet your best judgment of how obvious it can be before it becomes too intrusive and sits in front of the image; some users have called this a ‘fence’.”

As the experiment requires interactivity, we could not use the standard MTurk markup to create our HITs. Instead, we hosted a Flash application, presented to subjects in an embedded frame. The interface consisted of a chart display and alpha adjustment controls. “Lighter” and “Darker” buttons adjusted the alpha contrast by a value of 2 units on a 0-255 scale; holding a button resulted in an accelerated adjustment. By hosting the task ourselves, we were also able to use custom JavaScript to collect display configuration data, an option unavailable in the standard MTurk interface.

As a qualification task, subjects were asked to adjust a sample display so that the grid was fully transparent (alpha=0) or fully opaque (alpha=1), thereby ensuring that the subject could successfully run our Flash applet and adjust the grid contrast. We also considered eliciting additional display configuration information (such as monitor gamma), either by asking explicitly or with a calibration task. While a number of devices for facilitating user-provided perceptual estimates of monitor gamma exist, they are unreliable. For example, many LCD monitors are direction sensitive, with changes of viewing angle of just a few degrees causing a significant shift in perceived contrast. However, a rough estimate of gamma can be made using the web browser’s “User-Agent” field to infer the operating system: most PC systems use a gamma of 2.2 while Mac OS X (prior to 10.6) uses 1.8.

Crowdsourced Results  
![](images/a63444a9fb0ac2b321d80e5a1f1659208461fd7412ff130aacb46851108ec2a7.jpg)

![](images/1adc6575157068b9135d6e85078c68e6e83d3e46a52ceb75f8992e1bb48f84aa.jpg)  
Figure 8: Alpha contrast results (2L & 2D). Top: Stone & Bartram’s [30] lab study. Bottom: Our MTurk study. Error bars indicate 95% confidence intervals.

![](images/6ce08df751f2a7ca41c147abf1736a416d6b5721e8eff2ec20a8b67c174c0f2e.jpg)  
Figure 9: MTurk results for “Light” task (2L), grouped by operating system to estimate effect of monitor gamma.

We used a 5 (background) × 4 (density) factorial design with 3 replications, resulting in 60 trials (HITs) per task. Figures 6 and 7 illustrate these conditions. Each plot was sized at 450×300 pixels, and displayed within a frame 700 pixels tall. The background of the frame was varied with the trial and sized to fill the majority of a standard laptop display.

For each trial, we recorded the alpha value, time to completion, and the subject’s screen resolution, color depth, and browser type (“User-Agent”), as reported by JavaScript. We posted 60 HITs each for tasks L and D with N=24 assignments. Subjects were paid \$0.02 per HIT.