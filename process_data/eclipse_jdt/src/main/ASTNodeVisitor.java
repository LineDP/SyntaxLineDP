package main;
import java.util.ArrayList;
import java.util.List;
import org.eclipse.jdt.core.dom.ASTVisitor;
import org.eclipse.jdt.core.dom.MethodDeclaration;
import org.eclipse.jdt.core.dom.PackageDeclaration;
import org.eclipse.jdt.core.dom.ImportDeclaration;
import org.eclipse.jdt.core.dom.FieldDeclaration;
import org.eclipse.jdt.core.dom.TypeDeclaration;
import org.eclipse.jdt.core.dom.AnnotationTypeDeclaration;

public class ASTNodeVisitor extends ASTVisitor{
	List<MethodDeclaration> methodNodeList = new ArrayList<>();
	List<PackageDeclaration> packageNodeList = new ArrayList<>();
	List<ImportDeclaration> importNodeList = new ArrayList<>();
	List<FieldDeclaration> fieldNodeList = new ArrayList<>();
	List<TypeDeclaration> typeNodeList = new ArrayList<>();
	List<AnnotationTypeDeclaration> annotationNodeList = new ArrayList<>();

	public List<MethodDeclaration> getMethodDecs() {
		return methodNodeList;
	}
	
	public List<PackageDeclaration> getPackageDecs() {
		return packageNodeList;
	}
	
	public List<ImportDeclaration> getImportDecs() {
		return importNodeList;
	}
	
	public List<FieldDeclaration> getFieldDecs() {
		return fieldNodeList;
	}
	
	public List<TypeDeclaration> getTypeDecs() {
		return typeNodeList;
	}
	
	public List<AnnotationTypeDeclaration> getAnnotationDecs() {
		return annotationNodeList;
	}
	@Override
	public boolean visit(MethodDeclaration node) {
		methodNodeList.add(node);
		return true;
	}
	
	@Override
	public boolean visit(PackageDeclaration node) {
		packageNodeList.add(node);
		return true;
	}
	@Override
	public boolean visit(ImportDeclaration node) {
		importNodeList.add(node);
		return true;
	}
	@Override
	public boolean visit(FieldDeclaration node) {
		fieldNodeList.add(node);
		return true;
	}
	@Override
	public boolean visit(TypeDeclaration node) {
		typeNodeList.add(node);
		return true;
	}
	
	@Override
	public boolean visit(AnnotationTypeDeclaration node) {
		annotationNodeList.add(node);
		return true;
	}
}
