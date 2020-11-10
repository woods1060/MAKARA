from eprogress import LineProgress, CircleProgress, MultiProgressManager
import time
circle_progress = CircleProgress(title='circle loading')
for i in range(1, 101):
    circle_progress.update(i)
    time.sleep(0.1)

line_progress = LineProgress(title='line progress')
for i in range(1, 101):
    line_progress.update(i)
    time.sleep(0.05)
