package main;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.eclipse.jdt.core.dom.AST;
import org.eclipse.jdt.core.dom.ASTNode;
import org.eclipse.jdt.core.dom.ASTParser;
import org.eclipse.jdt.core.dom.CompilationUnit;
import org.eclipse.jdt.core.dom.MethodDeclaration;
import org.eclipse.jdt.core.dom.PackageDeclaration;
import org.eclipse.jdt.core.dom.ImportDeclaration;
import org.eclipse.jdt.core.dom.FieldDeclaration;
import org.eclipse.jdt.core.dom.TypeDeclaration;
import org.eclipse.jdt.core.dom.AnnotationTypeDeclaration;
import main.MethodNodeVisitor;
import main.ASTNodeVisitor;
import structure.MyMethodNode;
import structure.MyPackageNode;
import structure.MyASTNode;
import structure.MyImportNode;
import structure.MyFieldNode;
import structure.MyTypeNode;
import structure.MyAnnotationNode;
import util.FileUtil;

public class ASTGenerator {

	public List<MyMethodNode> methodNodeList = new ArrayList<MyMethodNode>();
	public List<MyPackageNode> packageNodeList = new ArrayList<MyPackageNode>();
	public List<MyImportNode> importNodeList = new ArrayList<MyImportNode>();
	public List<MyFieldNode> fieldNodeList = new ArrayList<MyFieldNode>();
	public List<MyTypeNode> typeNodeList = new ArrayList<MyTypeNode>();
	public List<MyAnnotationNode> annotationNodeList = new ArrayList<MyAnnotationNode>();

	public ASTGenerator(File f) {
		ParseFile(f);
	}
	public ASTGenerator(String code) {
		parse(code);
	}
	/**
	 * get function for methodNodeList
	 * @return
	 */
	public List<MyMethodNode> getMethodNodeList() {
		return methodNodeList;
	}
	
	public List<MyPackageNode> getPackageNodeList() {
		return packageNodeList;
	}
	
	public List<MyImportNode> getImportNodeList() {
		return importNodeList;
	}
	
	public List<MyFieldNode> getFieldNodeList() {
		return fieldNodeList;
	}
	public List<MyTypeNode> getTypeNodeList() {
		return typeNodeList;
	}
	
	public List<MyAnnotationNode> getAnnotationNodeList() {
		return annotationNodeList;
	}
	/**
	 * use ASTParse to parse string
	 * @param srcStr
	 */
	public void parse(String srcStr) {
		ASTParser parser = ASTParser.newParser(AST.JLS3);
		parser.setSource(srcStr.toCharArray());
		parser.setKind(ASTParser.K_COMPILATION_UNIT);
//		System.out.println(srcStr);
		final CompilationUnit cu = (CompilationUnit) parser.createAST(null);

		// find the MethodDeclaration node, MethodNodeVisitor
//		MethodNodeVisitor methodNodeVisitor = new MethodNodeVisitor();
		ASTNodeVisitor astNodeVisitor=new ASTNodeVisitor();
		cu.accept(astNodeVisitor);
		
		for (ImportDeclaration m : astNodeVisitor.getImportDecs()) {
			MyImportNode mNode = new MyImportNode();
			mNode.importNode = m;
			NodeVisitor nv = new NodeVisitor();
			m.accept(nv);
			List<ASTNode> astnodes = nv.getASTNodes();
			for (ASTNode node : astnodes) {
				MyASTNode myNode = new MyASTNode();
				myNode.astNode = node;
				myNode.startLineNum = cu.getLineNumber(node.getStartPosition());
				myNode.endLineNum = cu.getLineNumber(node.getStartPosition()+node.getLength());
				// add to nodeList
				mNode.nodeList.add(myNode);
				// add to mapping
				// in case, I need to exclude root node
				if (node.equals(m)) {
					continue;
				}
				int pHashcode = node.getParent().hashCode();
				int hashcode = node.hashCode();
				int[] link = { pHashcode, hashcode };
				mNode.mapping.add(link);
			}
			importNodeList.add(mNode);
		}
		
		for (PackageDeclaration m : astNodeVisitor.getPackageDecs()) {
			MyPackageNode mNode = new MyPackageNode();
			mNode.packageNode = m;
			NodeVisitor nv = new NodeVisitor();
			m.accept(nv);
			List<ASTNode> astnodes = nv.getASTNodes();
			for (ASTNode node : astnodes) {
				MyASTNode myNode = new MyASTNode();
				myNode.astNode = node;
				myNode.startLineNum = cu.getLineNumber(node.getStartPosition());
				myNode.endLineNum = cu.getLineNumber(node.getStartPosition()+node.getLength());
				// add to nodeList
				mNode.nodeList.add(myNode);
				// add to mapping
				// in case, I need to exclude root node
				if (node.equals(m)) {
					continue;
				}
				int pHashcode = node.getParent().hashCode();
				int hashcode = node.hashCode();
				int[] link = { pHashcode, hashcode };
				mNode.mapping.add(link);
			}
			packageNodeList.add(mNode);
		}
		
		
		for (TypeDeclaration m : astNodeVisitor.getTypeDecs()) {
			MyTypeNode mNode = new MyTypeNode();
			mNode.typeNode = m;
			NodeVisitor nv = new NodeVisitor();
			m.accept(nv);
			List<ASTNode> astnodes = nv.getASTNodes();
			for (ASTNode node : astnodes) {
				MyASTNode myNode = new MyASTNode();
				myNode.astNode = node;
				myNode.startLineNum = cu.getLineNumber(node.getStartPosition());
				myNode.endLineNum = cu.getLineNumber(node.getStartPosition()+node.getLength());
				// add to nodeList
				mNode.nodeList.add(myNode);
				// add to mapping
				// in case, I need to exclude root node
				if (node.equals(m)) {
					continue;
				}
				int pHashcode = node.getParent().hashCode();
				int hashcode = node.hashCode();
				int[] link = { pHashcode, hashcode };
				mNode.mapping.add(link);
			}
			typeNodeList.add(mNode);
		}
		
		for (AnnotationTypeDeclaration m : astNodeVisitor.getAnnotationDecs()) {
			MyAnnotationNode mNode = new MyAnnotationNode();
			mNode.annotationNode = m;
			NodeVisitor nv = new NodeVisitor();
			m.accept(nv);
			List<ASTNode> astnodes = nv.getASTNodes();
			for (ASTNode node : astnodes) {
				MyASTNode myNode = new MyASTNode();
				myNode.astNode = node;
				myNode.startLineNum = cu.getLineNumber(node.getStartPosition());
				myNode.endLineNum = cu.getLineNumber(node.getStartPosition()+node.getLength());
				// add to nodeList
				mNode.nodeList.add(myNode);
				// add to mapping
				// in case, I need to exclude root node
				if (node.equals(m)) {
					continue;
				}
				int pHashcode = node.getParent().hashCode();
				int hashcode = node.hashCode();
				int[] link = { pHashcode, hashcode };
				mNode.mapping.add(link);
			}
			annotationNodeList.add(mNode);
		}
		
		// traverse all child nodes, NodeVisitor
		for (MethodDeclaration m : astNodeVisitor.getMethodDecs()) {
			MyMethodNode mNode = new MyMethodNode();
			mNode.methodNode = m;
			NodeVisitor nv = new NodeVisitor();
			m.accept(nv);
			List<ASTNode> astnodes = nv.getASTNodes();
			for (ASTNode node : astnodes) {
				MyASTNode myNode = new MyASTNode();
				myNode.astNode = node;
				myNode.startLineNum = cu.getLineNumber(node.getStartPosition());
				myNode.endLineNum = cu.getLineNumber(node.getStartPosition()+node.getLength());
				// add to nodeList
				mNode.nodeList.add(myNode);
				// add to mapping
				// in case, I need to exclude root node
				if (node.equals(m)) {
					continue;
				}
				int pHashcode = node.getParent().hashCode();
				int hashcode = node.hashCode();
				int[] link = { pHashcode, hashcode };
				mNode.mapping.add(link);
			}
			methodNodeList.add(mNode);
		}
//		 System.out.println("");
	}

	public void ParseFile(File f) {
		String filePath = f.getAbsolutePath();
		if (f.isFile()) {
			try {
				parse(FileUtil.readFileToString(filePath));
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		} else {
			System.out.println("Not a File!");
		}
	}
}
