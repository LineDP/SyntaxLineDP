package structure;

import java.util.ArrayList;
import java.util.List;

import org.eclipse.jdt.core.dom.PackageDeclaration;
import structure.MyASTNode;

public class MyPackageNode {
	public PackageDeclaration packageNode = null;
	public List<MyASTNode> nodeList = null;

	public List<int[]> mapping = null;

	public MyPackageNode() {
		this.packageNode = null;
		this.nodeList = new ArrayList<MyASTNode>();
		this.mapping = new ArrayList<int[]>();
	}

}
