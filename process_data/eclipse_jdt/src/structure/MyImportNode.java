package structure;
import java.util.ArrayList;
import java.util.List;

import org.eclipse.jdt.core.dom.ImportDeclaration;
import structure.MyASTNode;

public class MyImportNode {
	public ImportDeclaration importNode = null;
	public List<MyASTNode> nodeList = null;

	public List<int[]> mapping = null;

	public MyImportNode() {
		this.importNode = null;
		this.nodeList = new ArrayList<MyASTNode>();
		this.mapping = new ArrayList<int[]>();
	}
}
