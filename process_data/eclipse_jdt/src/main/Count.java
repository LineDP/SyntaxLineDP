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
import java.util.*;

public class Count {
	
	private class DATA {
		private List<String> filename;
		private List<String> codelines;
		private List<String> is_test_file;
		private List<String> file_label;
		private List<String> line_label;
		private List<String> line_number;
	}
	
	
	public static void main(String[] args) throws IOException {
		String dir="C:\\Users\\Michael\\Desktop\\preprocessed_data2";
		File fileDir=new File(dir);
		File[] FileList=fileDir.listFiles();
		String outputpath="C:\\Users\\Michael\\Desktop\\count\\count.txt";
		File outfile=new File(outputpath);
		if(!outfile.exists()) {
			outfile.createNewFile();
		}
		OutputStream os=new FileOutputStream(outfile);
		Map<String,Integer> map=new HashMap<>();
		Map<String,Integer> map_global=new HashMap<>();
		for(File f:FileList) {
			try {
				BufferedReader reader=new BufferedReader(new FileReader(f));
				String release=f.getName();
				String tempString;
				
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
						ASTtoNodeType(m,map,map_global);
					}
					
					
					for(MyPackageNode m:packageNodeList) {
						ASTtoNodeType(m,map,map_global);
					}
					
					for(MyTypeNode m:typeNodeList) {
						ASTtoNodeType(m,map,map_global);
					}
//					if(typeNodeList.size()>0) {
//						MyTypeNode m1=typeNodeList.get(0);
//						ASTtoNodeType(m1,ast);
//					}
					
					
					
					for(MyAnnotationNode m:annotationNodeList) {
						ASTtoNodeType(m,map,map_global);
					}
//					if(annotationNodeList.size()>0) {
//						MyAnnotationNode m2=annotationNodeList.get(0);
//						ASTtoNodeType(m2,ast);
//					}
					
					
					
					
					
//					System.out.print(false);
				}
				
			} catch (FileNotFoundException e) {
				// TODO 自动生成的 catch 块
				e.printStackTrace();
			} catch (IOException e) {
				// TODO 自动生成的 catch 块
				e.printStackTrace();
			}
//			System.out.println();
		}
		OUT3 out=new OUT3(map);
		Gson gson=new Gson();
		String outString=gson.toJson(out)+"\n";
//		System.out.print(outString);
		
		byte[] bytes=outString.getBytes("UTF-8");
		os.write(bytes);
		
		OUT3 out2=new OUT3(map_global);
		String outString2=gson.toJson(out2)+"\n";
//		System.out.print(outString);
		
		byte[] bytes2=outString2.getBytes("UTF-8");
		os.write(bytes2);
		
		os.close();
	}
	
	@SuppressWarnings("unchecked")
	public static void ASTtoNodeType(MyAnnotationNode m, Map<String,Integer> data,Map<String,Integer> data_global) {
		for(MyASTNode mn:m.nodeList) {
			String nodeType=ASTNode.nodeClassForType(mn.astNode.getNodeType()).getName().replace("org.eclipse.jdt.core.dom.", "");
			
			int startLine=mn.startLineNum;
			int endLine=mn.endLineNum;
			
			if (startLine<0)continue;
			
			if(nodeType.equals("Javadoc"))continue;
			
			if(data_global.containsKey(nodeType)) {
				Integer old=data_global.get(nodeType);
				
				data_global.replace(nodeType, old+1);
			}
			else {
				data_global.put(nodeType, 1);
			}
			
			if (startLine!=endLine) {
				if(data.containsKey(nodeType)) {
					Integer old=data.get(nodeType);
					
					data.replace(nodeType, old+1);
				}
				else {
					data.put(nodeType, 1);
				}
			}
		}
	}
	
	@SuppressWarnings("unchecked")
	public static void ASTtoNodeType(MyTypeNode m, Map<String,Integer> data,Map<String,Integer> data_global) {
		for(MyASTNode mn:m.nodeList) {
			String nodeType=ASTNode.nodeClassForType(mn.astNode.getNodeType()).getName().replace("org.eclipse.jdt.core.dom.", "");
			
			int startLine=mn.startLineNum;
			int endLine=mn.endLineNum;
			
			if (startLine<0)continue;
			
			if(nodeType.equals("Javadoc"))continue;
			
			if(data_global.containsKey(nodeType)) {
				Integer old=data_global.get(nodeType);
				
				data_global.replace(nodeType, old+1);
			}
			else {
				data_global.put(nodeType, 1);
			}
			
			if (startLine!=endLine) {
				if(data.containsKey(nodeType)) {
					Integer old=data.get(nodeType);
					
					data.replace(nodeType, old+1);
				}
				else {
					data.put(nodeType, 1);
				}
			}
		}
	}
	
	@SuppressWarnings("unchecked")
	public static void ASTtoNodeType(MyPackageNode m, Map<String,Integer> data,Map<String,Integer> data_global) {
		for(MyASTNode mn:m.nodeList) {
			String nodeType=ASTNode.nodeClassForType(mn.astNode.getNodeType()).getName().replace("org.eclipse.jdt.core.dom.", "");
			
			int startLine=mn.startLineNum;
			int endLine=mn.endLineNum;
			
			if (startLine<0)continue;
			
			if(nodeType.equals("Javadoc"))continue;
			
			if(data_global.containsKey(nodeType)) {
				Integer old=data_global.get(nodeType);
				
				data_global.replace(nodeType, old+1);
			}
			else {
				data_global.put(nodeType, 1);
			}
			
			if (startLine!=endLine) {
				if(data.containsKey(nodeType)) {
					Integer old=data.get(nodeType);
					
					data.replace(nodeType, old+1);
				}
				else {
					data.put(nodeType, 1);
				}
			}
		}
	}
	
	@SuppressWarnings("unchecked")
	public static void ASTtoNodeType(MyImportNode m, Map<String,Integer> data,Map<String,Integer> data_global) {
		for(MyASTNode mn:m.nodeList) {
			String nodeType=ASTNode.nodeClassForType(mn.astNode.getNodeType()).getName().replace("org.eclipse.jdt.core.dom.", "");
			
			int startLine=mn.startLineNum;
			int endLine=mn.endLineNum;
			
			if (startLine<0)continue;
			
			if(nodeType.equals("Javadoc"))continue;
			
			if(data_global.containsKey(nodeType)) {
				Integer old=data_global.get(nodeType);
				
				data_global.replace(nodeType, old+1);
			}
			else {
				data_global.put(nodeType, 1);
			}
			
			if (startLine!=endLine) {
				if(data.containsKey(nodeType)) {
					Integer old=data.get(nodeType);
					
					data.replace(nodeType, old+1);
				}
				else {
					data.put(nodeType, 1);
				}
			}
		}
	}
	
	
}

