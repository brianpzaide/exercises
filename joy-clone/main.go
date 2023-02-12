package main

import (
	"fmt"
	"math"
	"strings"
)

const (
	Width  = 300
	Height = 300
)

var mainAttrs = map[string]string{
	"width":       fmt.Sprintf("%d", Width),
	"height":      fmt.Sprintf("%d", Height),
	"viewBox":     fmt.Sprintf("%d %d %d %d", -Width/2, -Height/2, Width, Height),
	"stroke":      "black",
	"xmlns":       "http://www.w3.org/2000/svg",
	"xmlns:xlink": "http://www.w3.org/1999/xlink",
}

var markers = []Shape{
	&Rect{x: -150, y: -150, width: 300, height: 300, tag: "rect", transforms: make([]Transformation, 0)},
	&Line{start: Point{X: -150, Y: 0}, end: Point{X: 150, Y: 0}, tag: "line", transforms: make([]Transformation, 0)},
	&Line{start: Point{X: 0, Y: -150}, end: Point{X: 0, Y: 150}, tag: "line", transforms: make([]Transformation, 0)},
}

type Point struct {
	X, Y int
}

type Shape interface {
	Clone() Shape
	Add(Shape) Shape
	Rotate(int, Point)
	Translate(Point)
	Scale(int, int)
	Cycle(int, Point, int, int, int) Shape
	Repeat(int, Transformation) Shape
	applyTransform(Transformation)
	As_str() string
	Show()
	get_attributes() map[string]string
	svg(string) string
}

type Transformation interface {
	As_str() string
	Join(Transformation) Transformation
}

// Circle implements Shape
type Circle struct {
	center     Point
	tag        string
	radius     int
	transforms []Transformation
}

func (c *Circle) Clone() Shape {
	newCircle := &Circle{
		center: c.center,
		tag:    c.tag,
		radius: c.radius,
	}

	newTransforms := make([]Transformation, 0)
	newTransforms = append(newTransforms, c.transforms...)
	newCircle.transforms = newTransforms

	return newCircle
}
func (c *Circle) Add(other Shape) Shape {
	grp := &Group{
		tag:        "g",
		shapes:     []Shape{c, other},
		transforms: make([]Transformation, 0),
	}
	return grp
}
func (c *Circle) Rotate(angle int, anchor Point) {
	transform := &Rotation{
		angle:  angle,
		anchor: anchor,
	}
	c.transforms = append(c.transforms, transform)
}
func (c *Circle) Translate(p Point) {
	transform := &Translation{
		x: p.X,
		y: p.Y,
	}
	c.transforms = append(c.transforms, transform)
}
func (c *Circle) Scale(sx, sy int) {
	transform := &Scale{
		sx: sx,
		sy: sy,
	}
	c.transforms = append(c.transforms, transform)
}
func (c *Circle) Cycle(n int, anchor Point, sx, sy int, angle int) Shape {
	grp := &Group{
		tag:        "g",
		shapes:     make([]Shape, 0),
		transforms: make([]Transformation, 0),
	}
	for i := 0; i < n; i++ {
		newShape := c.Clone()
		newAngle := i * angle
		newShape.Rotate(newAngle, anchor)
		newSx, newSy := int(math.Pow(float64(sx), float64(i))), int(math.Pow(float64(sy), float64(i)))
		newShape.Scale(newSx, newSy)
		grp.shapes = append(grp.shapes, newShape)
	}
	return grp
}
func (c *Circle) Repeat(n int, transformation Transformation) Shape {
	grp := &Group{
		tag:        "g",
		shapes:     make([]Shape, 0),
		transforms: make([]Transformation, 0),
	}
	for i := 0; i < n; i++ {
		newShape := c.Clone()
		newShape.applyTransform(transformation)
		grp.shapes = append(grp.shapes, newShape)
	}
	return grp
}
func (c *Circle) applyTransform(transformation Transformation) {
	switch trnsf := transformation.(type) {
	case *Rotation:
		c.Rotate(trnsf.angle, trnsf.anchor)
	case *Translation:
		c.Translate(Point{X: trnsf.x, Y: trnsf.y})
	case *Scale:
		c.Scale(trnsf.sx, trnsf.sy)
	}
}
func (c *Circle) As_str() string {
	return fmt.Sprintf(`<%s  cx="%d" cy="%d" r="%d" stroke="#ddd">`, c.tag, c.center.X, c.center.Y, c.radius)
}
func (c *Circle) Show() {
	fmt.Println(render(c))
}
func (c *Circle) get_attributes() map[string]string {
	attrs := make(map[string]string)
	attrs["cx"] = fmt.Sprintf("%d", c.center.X)
	attrs["cy"] = fmt.Sprintf("%d", c.center.Y)
	attrs["r"] = fmt.Sprintf("%d", c.radius)
	attrs["stroke"] = "#ddd"

	if len(c.transforms) > 0 {
		transformList := &TransformationList{transformations: c.transforms}
		attrs["transform"] = transformList.As_str()
	}

	return attrs
}
func (c *Circle) svg(indent string) string {
	attrs := c.get_attributes()
	tag_txt := render_tag(c.tag, true, attrs)
	return fmt.Sprintf("%s%s\n", indent, tag_txt)
}

// Line implements Shape
type Line struct {
	start      Point
	end        Point
	tag        string
	transforms []Transformation
}

func (l *Line) Clone() Shape {
	newLine := &Line{
		start: l.start,
		end:   l.end,
		tag:   l.tag,
	}

	newTransforms := make([]Transformation, 0)
	newTransforms = append(newTransforms, l.transforms...)
	newLine.transforms = newTransforms

	return newLine
}
func (l *Line) Add(other Shape) Shape {
	grp := &Group{
		tag:        "g",
		shapes:     []Shape{l, other},
		transforms: make([]Transformation, 0),
	}
	return grp
}
func (l *Line) Rotate(angle int, anchor Point) {
	transform := &Rotation{
		angle:  angle,
		anchor: anchor,
	}
	l.transforms = append(l.transforms, transform)
}
func (l *Line) Translate(p Point) {
	transform := &Translation{
		x: p.X,
		y: p.Y,
	}
	l.transforms = append(l.transforms, transform)
}
func (l *Line) Scale(sx, sy int) {
	transform := &Scale{
		sx: sx,
		sy: sy,
	}
	l.transforms = append(l.transforms, transform)
}
func (l *Line) Cycle(n int, anchor Point, sx, sy int, angle int) Shape {
	grp := &Group{
		tag:        "g",
		shapes:     make([]Shape, 0),
		transforms: make([]Transformation, 0),
	}
	for i := 0; i < n; i++ {
		newShape := l.Clone()
		newAngle := i * angle
		newShape.Rotate(newAngle, anchor)
		newSx, newSy := int(math.Pow(float64(sx), float64(i))), int(math.Pow(float64(sy), float64(i)))
		newShape.Scale(newSx, newSy)
		grp.shapes = append(grp.shapes, newShape)
	}
	return grp
}
func (l *Line) Repeat(n int, transformation Transformation) Shape {
	grp := &Group{
		tag:        "g",
		shapes:     make([]Shape, 0),
		transforms: make([]Transformation, 0),
	}
	for i := 0; i < n; i++ {
		newShape := l.Clone()
		newShape.applyTransform(transformation)
		grp.shapes = append(grp.shapes, newShape)
	}
	return grp
}
func (l *Line) applyTransform(transformation Transformation) {
	switch trnsf := transformation.(type) {
	case *Rotation:
		l.Rotate(trnsf.angle, trnsf.anchor)
	case *Translation:
		l.Translate(Point{X: trnsf.x, Y: trnsf.y})
	case *Scale:
		l.Scale(trnsf.sx, trnsf.sy)
	}
}
func (l *Line) As_str() string {
	return fmt.Sprintf(`<%s  x1="%d" y1="%d" x2="%d" y2="%d" stroke="#ddd">`, l.tag, l.start.X, l.start.Y, l.end.X, l.end.Y)
}
func (l *Line) Show() {
	fmt.Println(render(l))
}
func (l *Line) get_attributes() map[string]string {
	attrs := make(map[string]string)
	attrs["x1"] = fmt.Sprintf("%d", l.start.X)
	attrs["y1"] = fmt.Sprintf("%d", l.start.Y)
	attrs["x2"] = fmt.Sprintf("%d", l.end.X)
	attrs["y2"] = fmt.Sprintf("%d", l.end.Y)
	attrs["stroke"] = "#ddd"

	if len(l.transforms) > 0 {
		transformList := &TransformationList{transformations: l.transforms}
		attrs["transform"] = transformList.As_str()
	}

	return attrs
}
func (l *Line) svg(indent string) string {
	attrs := l.get_attributes()
	tag_txt := render_tag(l.tag, true, attrs)
	return fmt.Sprintf("%s%s\n", indent, tag_txt)
}

// Rect implements Shape
type Rect struct {
	x, y          int
	width, height int
	tag           string
	transforms    []Transformation
}

func (r *Rect) Clone() Shape {
	newRect := &Rect{
		x:      r.x,
		y:      r.y,
		width:  r.width,
		height: r.height,
		tag:    r.tag,
	}

	newTransforms := make([]Transformation, 0)
	newTransforms = append(newTransforms, r.transforms...)
	newRect.transforms = newTransforms

	return newRect
}
func (r *Rect) Add(other Shape) Shape {
	grp := &Group{
		tag:        "g",
		shapes:     []Shape{r, other},
		transforms: make([]Transformation, 0),
	}
	return grp
}
func (r *Rect) Rotate(angle int, anchor Point) {
	transform := &Rotation{
		angle:  angle,
		anchor: anchor,
	}
	r.transforms = append(r.transforms, transform)
}
func (r *Rect) Translate(p Point) {
	transform := &Translation{
		x: p.X,
		y: p.Y,
	}
	r.transforms = append(r.transforms, transform)
}
func (r *Rect) Scale(sx, sy int) {
	transform := &Scale{
		sx: sx,
		sy: sy,
	}
	r.transforms = append(r.transforms, transform)
}
func (r *Rect) Cycle(n int, anchor Point, sx, sy int, angle int) Shape {
	grp := &Group{
		tag:        "g",
		shapes:     make([]Shape, 0),
		transforms: make([]Transformation, 0),
	}
	for i := 0; i < n; i++ {
		newShape := r.Clone()
		newAngle := i * angle
		newShape.Rotate(newAngle, anchor)
		newSx, newSy := int(math.Pow(float64(sx), float64(i))), int(math.Pow(float64(sy), float64(i)))
		newShape.Scale(newSx, newSy)
		grp.shapes = append(grp.shapes, newShape)
	}
	return grp
}
func (r *Rect) Repeat(n int, transformation Transformation) Shape {
	grp := &Group{
		tag:        "g",
		shapes:     make([]Shape, 0),
		transforms: make([]Transformation, 0),
	}
	for i := 0; i < n; i++ {
		newShape := r.Clone()
		newShape.applyTransform(transformation)
		grp.shapes = append(grp.shapes, newShape)
	}
	return grp
}
func (r *Rect) applyTransform(transformation Transformation) {
	switch trnsf := transformation.(type) {
	case *Rotation:
		r.Rotate(trnsf.angle, trnsf.anchor)
	case *Translation:
		r.Translate(Point{X: trnsf.x, Y: trnsf.y})
	case *Scale:
		r.Scale(trnsf.sx, trnsf.sy)
	}
}
func (r *Rect) As_str() string {
	return fmt.Sprintf(`<%s  x="%d" y="%d" width="%d" height="%d" stroke="#ddd">`, r.tag, r.x, r.y, r.width, r.height)
}
func (r *Rect) Show() {
	fmt.Println(render(r))
}
func (r *Rect) get_attributes() map[string]string {
	attrs := make(map[string]string)
	attrs["x"] = fmt.Sprintf("%d", r.x)
	attrs["y"] = fmt.Sprintf("%d", r.y)
	attrs["width"] = fmt.Sprintf("%d", r.width)
	attrs["height"] = fmt.Sprintf("%d", r.height)
	attrs["stroke"] = "#ddd"

	if len(r.transforms) > 0 {
		transformList := &TransformationList{transformations: r.transforms}
		attrs["transform"] = transformList.As_str()
	}

	return attrs
}
func (r *Rect) svg(indent string) string {
	attrs := r.get_attributes()
	tag_txt := render_tag(r.tag, true, attrs)
	return fmt.Sprintf("%s%s\n", indent, tag_txt)
}

// Ellipse implements Shape
type Ellipse struct {
	center        Point
	width, height int
	tag           string
	transforms    []Transformation
}

func (e *Ellipse) Clone() Shape {
	newEllipse := &Ellipse{
		center: e.center,
		width:  e.width,
		height: e.height,
		tag:    e.tag,
	}

	newTransforms := make([]Transformation, 0)
	newTransforms = append(newTransforms, e.transforms...)
	newEllipse.transforms = newTransforms

	return newEllipse
}
func (e *Ellipse) Add(other Shape) Shape {
	grp := &Group{
		tag:        "g",
		shapes:     []Shape{e, other},
		transforms: make([]Transformation, 0),
	}
	return grp
}
func (e *Ellipse) Rotate(angle int, anchor Point) {
	transform := &Rotation{
		angle:  angle,
		anchor: anchor,
	}
	e.transforms = append(e.transforms, transform)
}
func (e *Ellipse) Translate(p Point) {
	transform := &Translation{
		x: p.X,
		y: p.Y,
	}
	e.transforms = append(e.transforms, transform)
}
func (e *Ellipse) Scale(sx, sy int) {
	transform := &Scale{
		sx: sx,
		sy: sy,
	}
	e.transforms = append(e.transforms, transform)
}
func (e *Ellipse) Cycle(n int, anchor Point, sx, sy int, angle int) Shape {
	grp := &Group{
		tag:        "g",
		shapes:     make([]Shape, 0),
		transforms: make([]Transformation, 0),
	}
	for i := 0; i < n; i++ {
		newShape := e.Clone()
		newAngle := i * angle
		newShape.Rotate(newAngle, anchor)
		newSx, newSy := int(math.Pow(float64(sx), float64(i))), int(math.Pow(float64(sy), float64(i)))
		newShape.Scale(newSx, newSy)
		grp.shapes = append(grp.shapes, newShape)
	}
	return grp
}
func (e *Ellipse) Repeat(n int, transformation Transformation) Shape {
	grp := &Group{
		tag:        "g",
		shapes:     make([]Shape, 0),
		transforms: make([]Transformation, 0),
	}
	for i := 0; i < n; i++ {
		newShape := e.Clone()
		newShape.applyTransform(transformation)
		grp.shapes = append(grp.shapes, newShape)
	}
	return grp
}
func (e *Ellipse) applyTransform(transformation Transformation) {
	switch trnsf := transformation.(type) {
	case *Rotation:
		e.Rotate(trnsf.angle, trnsf.anchor)
	case *Translation:
		e.Translate(Point{X: trnsf.x, Y: trnsf.y})
	case *Scale:
		e.Scale(trnsf.sx, trnsf.sy)
	}
}
func (e *Ellipse) As_str() string {
	return fmt.Sprintf(`<%s  cx="%d" cy="%d" rx="%d" ry="%d" stroke="#ddd">`, e.tag, e.center.X, e.center.Y, e.width, e.height)
}
func (e *Ellipse) Show() {
	fmt.Println(render(e))
}
func (e *Ellipse) get_attributes() map[string]string {
	attrs := make(map[string]string)
	attrs["cx"] = fmt.Sprintf("%d", e.center.X)
	attrs["cy"] = fmt.Sprintf("%d", e.center.Y)
	attrs["rx"] = fmt.Sprintf("%d", e.width)
	attrs["ry"] = fmt.Sprintf("%d", e.height)
	attrs["stroke"] = "#ddd"

	if len(e.transforms) > 0 {
		transformList := &TransformationList{transformations: e.transforms}
		attrs["transform"] = transformList.As_str()
	}

	return attrs
}
func (e *Ellipse) svg(indent string) string {
	attrs := e.get_attributes()
	tag_txt := render_tag(e.tag, true, attrs)
	return fmt.Sprintf("%s%s\n", indent, tag_txt)
}

// Group implements Shape
type Group struct {
	shapes     []Shape
	tag        string
	transforms []Transformation
}

func (g *Group) Clone() Shape {
	newGroup := &Group{
		tag: g.tag,
	}

	newTransforms := make([]Transformation, 0)
	newTransforms = append(newTransforms, g.transforms...)
	newGroup.transforms = newTransforms

	clonedShapes := make([]Shape, 0)
	for _, shape := range g.shapes {
		clonedShapes = append(clonedShapes, shape.Clone())
	}
	newGroup.shapes = clonedShapes

	return newGroup
}
func (g *Group) Add(other Shape) Shape {
	grp := &Group{
		tag:        "g",
		shapes:     []Shape{g, other},
		transforms: make([]Transformation, 0),
	}
	return grp
}
func (g *Group) Rotate(angle int, anchor Point) {
	transform := &Rotation{
		angle:  angle,
		anchor: anchor,
	}
	g.transforms = append(g.transforms, transform)
}
func (g *Group) Translate(p Point) {
	transform := &Translation{
		x: p.X,
		y: p.Y,
	}
	g.transforms = append(g.transforms, transform)
}
func (g *Group) Scale(sx, sy int) {
	transform := &Scale{
		sx: sx,
		sy: sy,
	}
	g.transforms = append(g.transforms, transform)
}
func (g *Group) Cycle(n int, anchor Point, sx, sy int, angle int) Shape {
	grp := &Group{
		tag:        "g",
		shapes:     make([]Shape, 0),
		transforms: make([]Transformation, 0),
	}
	for i := 0; i < n; i++ {
		newShape := g.Clone()
		newAngle := i * angle
		newShape.Rotate(newAngle, anchor)
		newSx, newSy := int(math.Pow(float64(sx), float64(i))), int(math.Pow(float64(sy), float64(i)))
		newShape.Scale(newSx, newSy)
		grp.shapes = append(grp.shapes, newShape)
	}
	return grp
}
func (g *Group) Repeat(n int, transformation Transformation) Shape {
	grp := &Group{
		tag:        "g",
		shapes:     make([]Shape, 0),
		transforms: make([]Transformation, 0),
	}
	for i := 0; i < n; i++ {
		newShape := g.Clone()
		newShape.applyTransform(transformation)
		grp.shapes = append(grp.shapes, newShape)
	}
	return grp
}
func (g *Group) applyTransform(transformation Transformation) {
	switch trnsf := transformation.(type) {
	case *Rotation:
		g.Rotate(trnsf.angle, trnsf.anchor)
	case *Translation:
		g.Translate(Point{X: trnsf.x, Y: trnsf.y})
	case *Scale:
		g.Scale(trnsf.sx, trnsf.sy)
	}
}
func (g *Group) As_str() string {
	return fmt.Sprintf(`<%s>`, g.tag)
}
func (g *Group) Show() {
	fmt.Println(render(g))
}

func (g *Group) get_attributes() map[string]string {
	attrs := make(map[string]string)

	attrs["stroke"] = "#ddd"

	if len(g.transforms) > 0 {
		transformList := &TransformationList{transformations: g.transforms}
		attrs["transform"] = transformList.As_str()
	}
	return attrs
}

// TODO render tags for each shape in g.shapes
func (g *Group) svg(indent string) string {
	attrs := g.get_attributes()
	var toClose bool
	if len(g.shapes) == 0 {
		toClose = true
	} else {
		toClose = false
	}
	tag_txt := render_tag(g.tag, toClose, attrs)
	var shapesTxt strings.Builder
	shapesTxt.WriteString("\n")
	for _, sh := range g.shapes {
		shapesTxt.WriteString(sh.svg(indent+" ") + "\n")
	}
	if toClose {
		return fmt.Sprintf("%s%s\n", indent, tag_txt)
	}
	return fmt.Sprintf("%s%s%s%s</%s>\n", indent, tag_txt, shapesTxt.String(), indent, g.tag)

}

// Rotation implements Transformation
type Rotation struct {
	angle  int
	anchor Point
}

func (r *Rotation) As_str() string {
	if r.anchor.X == 0 && r.anchor.Y == 0 {
		return fmt.Sprintf(`rotate(%d)`, r.angle)
	}
	return fmt.Sprintf(`rotate(%d %d %d)`, r.angle, r.anchor.X, r.anchor.Y)
}
func (r *Rotation) Join(other Transformation) Transformation {
	return &TransformationList{transformations: []Transformation{r, other}}
}

// Translation implements Transformation
type Translation struct {
	x, y int
}

func (t *Translation) As_str() string {
	return fmt.Sprintf(`translate(%d %d)`, t.x, t.y)
}
func (t *Translation) Join(other Transformation) Transformation {
	return &TransformationList{transformations: []Transformation{t, other}}
}

// Scale implements Transformation
type Scale struct {
	sx, sy int
}

func (s *Scale) As_str() string {
	return fmt.Sprintf(`scale(%d %d)`, s.sx, s.sy)
}
func (s *Scale) Join(other Transformation) Transformation {
	return &TransformationList{transformations: []Transformation{s, other}}
}

// TransformationList implements Transformation
type TransformationList struct {
	transformations []Transformation
}

func (tl *TransformationList) As_str() string {
	var transforms_txt strings.Builder
	n := len(tl.transformations)
	for i, tr := range tl.transformations {
		if i < n-1 {
			transforms_txt.WriteString(tr.As_str() + " ")
		} else {
			transforms_txt.WriteString(tr.As_str())
		}

	}
	return transforms_txt.String()
}
func (tl *TransformationList) Join(other Transformation) Transformation {
	return &TransformationList{transformations: []Transformation{tl, other}}
}

func render(s Shape) string {
	svgHeader := render_tag("svg", false, mainAttrs) + "\n"
	svgFooter := `</svg>` + "\n"
	shapes := make([]Shape, 0)
	shapes = append(shapes, markers...)
	shapes = append(shapes, s)
	g := &Group{tag: "g", shapes: shapes}
	g.Scale(1, -1)
	// fmt.Println(svgHeader)
	// fmt.Println(g.svg(""))
	// fmt.Println(svgFooter)
	return svgHeader + g.svg("") + svgFooter
}

func render_tag(tag string, toClose bool, attrs map[string]string) string {
	var end string
	if toClose {
		end = "/>"
	} else {
		end = ">"
	}
	var attrsTxt strings.Builder
	attrsTxt.WriteString(fmt.Sprintf(`<%s `, tag))
	if len(attrs) > 0 {
		i, n := 0, len(attrs)
		for k, v := range attrs {
			if i < n-1 {
				attrsTxt.WriteString(fmt.Sprintf(`%s="%s" `, k, v))
			} else {
				attrsTxt.WriteString(fmt.Sprintf(`%s="%s"`, k, v))
			}
		}
		attrsTxt.WriteString(end)
		return attrsTxt.String()
	} else {
		return fmt.Sprintf("<%s %s\n", tag, end)
	}
}

func main() {
	shapes := []Shape{
		&Ellipse{tag: "ellipse", center: Point{0, 0}, width: 100, height: 50},
		&Circle{tag: "circle", center: Point{0, 0}, radius: 50},
		&Rect{tag: "rect", x: -20, y: -20, width: 40, height: 40},
	}
	g := &Group{tag: "g", shapes: shapes, transforms: make([]Transformation, 0)}

	var shapesTxt strings.Builder
	var transformsTxt strings.Builder

	for _, sh := range g.shapes {
		shapesTxt.WriteString(sh.As_str() + "\n")
	}

	for _, tr := range g.transforms {
		transformsTxt.WriteString(tr.As_str() + "\n")
	}

	// fmt.Printf("tag:%s\nshapes:\n%s\ntransforms:\n%s", g.tag, shapesTxt.String(), transformsTxt.String())
	g.Show()
}
