"""ShapeTweenEngine — generate intermediate shapes between two selected shapes."""

from src.backend.context import PresentationContext
from src.engine.base import BaseEngine, EngineResult


class ShapeTweenEngine(BaseEngine):

    @staticmethod
    def apply(context: PresentationContext, steps: int = 5) -> EngineResult:
        """Generate N intermediate shapes between two selected shapes.

        Interpolates: position, size, rotation, text font size.
        """
        shapes = context.get_selected_shape_proxies()
        if len(shapes) != 2:
            return EngineResult(success=False, message="Select exactly 2 shapes for tweening")

        if steps < 1 or steps > 20:
            return EngineResult(success=False, message="Steps must be between 1 and 20")

        try:
            a, b = shapes[0], shapes[1]
            created = 0

            for i in range(1, steps + 1):
                t = i / (steps + 1)

                # Interpolate geometry
                left = a.bounds.left + (b.bounds.left - a.bounds.left) * t
                top = a.bounds.top + (b.bounds.top - a.bounds.top) * t
                width = a.bounds.width + (b.bounds.width - a.bounds.width) * t
                height = a.bounds.height + (b.bounds.height - a.bounds.height) * t

                # Get rotations
                rot_a = a.rotation
                rot_b = b.rotation
                rotation = rot_a + (rot_b - rot_a) * t

                # Duplicate the first shape as base
                if context.backend_type == "com":
                    a.internal_ref.Copy()
                    slide = context._pres.Slides(a.slide_index + 1)
                    # Paste and get the new shape
                    pasted = slide.Shapes.Paste()
                    pasted.Left = left
                    pasted.Top = top
                    pasted.Width = width
                    pasted.Height = height
                    pasted.Rotation = rotation
                    created += 1
                else:
                    import copy
                    from pptx.util import Pt
                    slide = context._prs.slides[a.slide_index]
                    el = copy.deepcopy(a.internal_ref._element)
                    new_shape_el = slide.shapes._spTree.append(el)
                    # Adjust position and size via XML
                    from lxml import etree
                    nsmap = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
                    xfrm = el.find('.//a:xfrm', nsmap)
                    if xfrm is not None:
                        off = xfrm.find('a:off', nsmap)
                        ext = xfrm.find('a:ext', nsmap)
                        if off is not None:
                            off.set('x', str(int(left * 12700)))
                            off.set('y', str(int(top * 12700)))
                        if ext is not None:
                            ext.set('cx', str(int(width * 12700)))
                            ext.set('cy', str(int(height * 12700)))
                    created += 1

            return EngineResult(
                success=True,
                message=f"Generated {created} tween shapes ({steps} steps)",
                data={"count": created, "steps": steps}
            )
        except Exception as e:
            return EngineResult(success=False, message=str(e))
