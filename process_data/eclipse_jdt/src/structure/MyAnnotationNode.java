package structure;

import java.util.ArrayList;
import java.util.List;

import org.eclipse.jdt.core.dom.AnnotationTypeDeclaration;

public class MyAnnotationNode {
	public AnnotationTypeDeclaration annotationNode = null;
	public List<MyASTNode> nodeList = null;

	public List<int[]> mapping = null;

	public MyAnnotationNode() {
		this.annotationNode = null;
		this.nodeList = new ArrayList<MyASTNode>();
		this.mapping = new ArrayList<int[]>();
	}
}
