from PySide2.QtCore import QByteArray
from PySide2.QtGui import QPixmap


def app_icon():
    base64data = b"iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAABmJLR0QA/wD/AP+gvaeTAAAFKklEQVRoge2ZX4hUVRzHP79z7+zu6LpQaLq6aEZhkT1krJT4uiD" \
                 b"+eREMIShB8CV8aXsoIpKEHkJfwreUIIgKS8ECwfBF7MHQp6woKLa0NXUVl3V3Zu7cc3493Htn7syd2dmdpv0D+4Uzc+9vZs75fn/f3zn33DuwhCUsYQnzCelUR/+8vPkDlGGgq8VXA5Rja766" \
                 b"/k4nxjWd6ATAOR12ql1OlRaty6HDnRrX71RHo5PlVplPo7tT4zYsoe/3bhscWLXizMq+3nU53+tYmbWDcmh1bGLi1p3x8QODn1/5rv7zDLkf9g4ObupfeaUrN7/E6xGUrf5y5/7gi6evXEvHMyW0crl" \
                 b"/xtdAXDB35GYCH+SxLjkLrK+L1+JRX9a5oDRnxGaDR7pkoD6WEWDUioZ2bhjNEl6Dks8IcGE4N2w6hOwy6hZm9pshI0Cdmw8ebSPrgC5yAYvNgY7theYLi15AgzmgHem45/gwLM9HJw8LFN883pF+6/H" \
                 b"/OZCQB+jNN//ef0TGAauKkc7v4zrhq23QScaBO4UOXYkfFhof/wfcLZQzsYwDt6fKPCiF5D1Dty90G0O3J+Q9w2yMKQwfa5uoKhSso2SVknOUQqVglaDBEp8R4AkETilZiwsUVXCAU" \
                 b"/AM9HhCj2foNoYeT1jmG/K+aevmOnDKVOgoxkSLoaNoHWULItHOzQgIgpHoeAYCBEFxRD9UQFBMnJmpsjJZtighqtXaznuGbs+Q9yNRPUbI" \
                 b"+1GFFkJHMSEbKkXrKDgHGpGMnJVKEkSi2jYieGkhDUogu52OFQugaCwgEqKAEY2JCypURJSco+Qc4y1uhJLMeggi0W+tKqrV0YyAE/AUMJATEznQoL" \
                 b"+GDigaC6g6UCVbFaNxCqNLRxRHmq84UvceqkZt4zMUd++nvGU7tn8AFMytm/jXLrPi/Bf0" \
                 b"/vkrokLOZCVkPLk6tFGVqOaV6hxQEgFaOaYiJHqpJV4vQ2oGLKsSeDkmD79HsOcVnJjqGArWRRystfR98xnrTh0l70JeujhSw3lGDhjAJcRjCjUuACpVzto4NzXkrZ9j4sNPCZ" \
                 b"/fFierAXkFi8e93a9SGHiSp98/kOkz44knkQgvnkCeiWK+SKXVx70kbqrH6Xj6XCRKyuThI63JJ8cOHjy3jT9eyz7My6Tpxx1PaLokGpVOfdloKu81hZOcpEYpO2Vywybufny" \
                 b"+ednUkbcK1kIYWgLrbT7aLz81dcDETeJ112RcSTKbdoFUvJptz9S64okAwtTO/bMn7yDEQ4WDab6ZOSCSLKGgqpWlTuLBqqtMatWpqf2MDxU4FQxKccv22ZN3USx0DE0rwMSEBFCpTlg0WkrT9JIyoi7e" \
                 b"/KG3YgTC1WvbJU/o2DCtgOTKmM56IiZxRjRV7ynyrbYTmvTt2iaPdbX2Nr0fEKqXcJOaD8klXkQwzRo0bmKiuXF3tF3yhI6" \
                 b"/Wgm42VSQ1AmSZOtRT7SxsFw84Zddu9weeQuh5cL0ApRDwI1mztQ7lHGpRcsZYdWFL7HWzpq8teqKjlP1POYFH03qCae8PuPMOxh7MPHt6Rf69qT7mbenEveX8Ya1XJwp+dHbY1z//e" \
                 b"+hrZfGdy0IAUdEgok+dlrLidBhpyFv741PnPvt5lipd/Xa7nLZvb3m5EhFxIL4F+bdW/qsCgdDx1DoeDwWMhJaLhQdpz55Sn7eeml8VxC4t26PPBxEVUTZN3po" \
                 b"/bkFIWCm6D95YweqZ4EeIBBl36ISALDm5MguUfM10T+dVxedAKiIOBL6ds+/q51uO36SnGsAAAAASUVORK5CYII= "
    ba = QByteArray.fromBase64(base64data)
    icon_img = QPixmap()
    icon_img.loadFromData(ba)
    return icon_img
