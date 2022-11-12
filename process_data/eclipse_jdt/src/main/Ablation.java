package main;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.regex.*;
import org.eclipse.jdt.core.dom.ASTNode;
import net.sf.json.JSONObject;
import structure.MyMethodNode;
import structure.MyPackageNode;
import structure.MyASTNode;
import structure.MyImportNode;
import structure.MyFieldNode;
import structure.MyTypeNode;
import structure.MyAnnotationNode;
import jxl.Cell;
import jxl.Sheet;
import jxl.Workbook;
import jxl.read.biff.BiffException;
import com.google.gson.Gson;
import com.google.gson.JsonElement;

//不添加任何语法覆盖信息
public class Ablation {
	
	private class DATA {
		private List<String> filename;
		private List<String> codelines;
		private List<String> is_test_file;
		private List<String> file_label;
		private List<String> line_label;
		private List<String> line_number;
	}
	
	
	public static void main(String[] args) {
		String dir="../../../../Datasets/preprocessed_data2";
		File fileDir=new File(dir);
		File[] FileList=fileDir.listFiles();
		for(File f:FileList) {
			try {
				BufferedReader reader=new BufferedReader(new FileReader(f));
				String release=f.getName();
				String tempString;
				String outputpath="../../../../Datasets/add_syntax/nothing/"+release;
				File outfile=new File(outputpath);
				if(!outfile.exists()) {
					outfile.createNewFile();
				}
				OutputStream os=new FileOutputStream(outfile);
				
				while((tempString=reader.readLine())!=null) {
					Gson gson=new Gson();
					DATA data=gson.fromJson(tempString, DATA.class);
					String code="";
					int num=data.codelines.size(),i=0;
					List[] ast=new List[num];
					
					for(String line:data.codelines) {
						code+=line+"\n";
						ast[i++]=new ArrayList();
					}
//					System.out.println(code);
					ASTGenerator astGenerator=new ASTGenerator(code);
					List<MyMethodNode> methodNodeList =astGenerator.getMethodNodeList();
					List<MyImportNode> importNodeList =astGenerator.getImportNodeList();
					List<MyPackageNode> packageNodeList =astGenerator.getPackageNodeList();
					List<MyTypeNode> typeNodeList =astGenerator.getTypeNodeList();
					List<MyAnnotationNode> annotationNodeList =astGenerator.getAnnotationNodeList();
					for(MyImportNode m:importNodeList) {
						ASTtoNodeType(m,ast);
					}
					
					for(MyPackageNode m:packageNodeList) {
						ASTtoNodeType(m,ast);
					}
					
					for(MyTypeNode m:typeNodeList) {
						ASTtoNodeType(m,ast);
					}
//					if(typeNodeList.size()>0) {
//						MyTypeNode m1=typeNodeList.get(0);
//						ASTtoNodeType(m1,ast);
//					}
					
					
					
					for(MyAnnotationNode m:annotationNodeList) {
						ASTtoNodeType(m,ast);
					}
//					if(annotationNodeList.size()>0) {
//						MyAnnotationNode m2=annotationNodeList.get(0);
//						ASTtoNodeType(m2,ast);
//					}
					
					
					
					OUT out=new OUT(data.filename,data.codelines,data.is_test_file,data.file_label,data.line_label,data.line_number,ast);
					String outString=gson.toJson(out)+"\n";
//					System.out.print(outString);
					
					byte[] bytes=outString.getBytes("UTF-8");
					os.write(bytes);
					
//					System.out.print(false);
				}
				
				os.close();
			} catch (FileNotFoundException e) {
				// TODO 自动生成的 catch 块
				e.printStackTrace();
			} catch (IOException e) {
				// TODO 自动生成的 catch 块
				e.printStackTrace();
			}
//			System.out.println();
		}
	}
	
	@SuppressWarnings("unchecked")
	public static void ASTtoNodeType(MyAnnotationNode m, List[] data) {
		for(MyASTNode mn:m.nodeList) {
			String nodeType=ASTNode.nodeClassForType(mn.astNode.getNodeType()).getName().replace("org.eclipse.jdt.core.dom.", "");
			
			int startLine=mn.startLineNum;
			int endLine=mn.endLineNum;
			
			if (startLine<0)continue;
			
			if(nodeType.equals("Javadoc"))continue;
//			if(nodeType.equals("SimpleName")) {
//				System.out.println(mn.astNode.toString());
//				System.out.println(mn.astNode.getLength());
//			}
			data[startLine-1].add(nodeType);
			if(nodeType.equals("SimpleName")) {
				data[startLine-1].add(mn.astNode.toString());
			}
			
		}
	}
	
	@SuppressWarnings("unchecked")
	public static void ASTtoNodeType(MyTypeNode m, List[] data) {
		for(MyASTNode mn:m.nodeList) {
			String nodeType=ASTNode.nodeClassForType(mn.astNode.getNodeType()).getName().replace("org.eclipse.jdt.core.dom.", "");
			
			int startLine=mn.startLineNum;
			int endLine=mn.endLineNum;
			
			if (startLine<0)continue;
			if(nodeType.equals("Javadoc"))continue;
//			if(nodeType.equals("SimpleName")) {
//				System.out.println(mn.astNode.toString());
//				System.out.println(mn.astNode.getLength());
//			}
			data[startLine-1].add(nodeType);
			if(nodeType.equals("SimpleName")) {
				data[startLine-1].add(mn.astNode.toString());
			}
		}
	}
	
	@SuppressWarnings("unchecked")
	public static void ASTtoNodeType(MyPackageNode m, List[] data) {
		for(MyASTNode mn:m.nodeList) {
			String nodeType=ASTNode.nodeClassForType(mn.astNode.getNodeType()).getName().replace("org.eclipse.jdt.core.dom.", "");
			
			int startLine=mn.startLineNum;
			int endLine=mn.endLineNum;
			
			if(nodeType.equals("Javadoc"))continue;
//			if(nodeType.equals("SimpleName")) {
//				System.out.println(mn.astNode.toString());
//				System.out.println(mn.astNode.getLength());
//			}
			data[startLine-1].add(nodeType);
			if(nodeType.equals("SimpleName")) {
				data[startLine-1].add(mn.astNode.toString());
			}
		}
	}
	
	@SuppressWarnings("unchecked")
	public static void ASTtoNodeType(MyImportNode m, List[] data) {
		for(MyASTNode mn:m.nodeList) {
			String nodeType=ASTNode.nodeClassForType(mn.astNode.getNodeType()).getName().replace("org.eclipse.jdt.core.dom.", "");
			
			int startLine=mn.startLineNum;
			int endLine=mn.endLineNum;
			
			if(nodeType.equals("Javadoc"))continue;
//			if(nodeType.equals("SimpleName")) {
//				System.out.println(mn.astNode.toString());
//				System.out.println(mn.astNode.getLength());
//			}
			data[startLine-1].add(nodeType);
			if(nodeType.equals("SimpleName")) {
				data[startLine-1].add(mn.astNode.toString());
			}
		}
	}
	
	@SuppressWarnings("unchecked")
	public static void ASTtoNodeType(MyMethodNode m, List[] data) {
		for(MyASTNode mn:m.nodeList) {
			String nodeType=ASTNode.nodeClassForType(mn.astNode.getNodeType()).getName().replace("org.eclipse.jdt.core.dom.", "");
			
			int startLine=mn.startLineNum;
			int endLine=mn.endLineNum;
			
			if(nodeType.equals("Javadoc"))continue;
//			if(nodeType.equals("SimpleName")) {
//				System.out.println(mn.astNode.toString());
//				System.out.println(mn.astNode.getLength());
//			}
			data[startLine-1].add(nodeType);
			if(nodeType.equals("SimpleName")) {
				data[startLine-1].add(mn.astNode.toString());
			}
		}
	}
	
}

